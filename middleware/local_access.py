"""로컬 접근만 허용하는 미들웨어"""

import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class LocalAccessMiddleware(BaseHTTPMiddleware):
    """
    로컬 IP 주소에서의 접근만 허용하는 미들웨어

    Starlette의 BaseHTTPMiddleware를 상속받아 구현
    """

    ALLOWED_LOCAL_IPS = ["127.0.0.1", "0.0.0.0", "localhost", "192.168.0.100"]

    def __init__(self, app):
        """
        Args:
            app: ASGI 애플리케이션
            allowed_ips: 추가로 허용할 IP 주소 리스트 (기본값: None)
        """
        super().__init__(app)

    def _is_local_ip(self, client_ip: str) -> bool:
        """
        IP 주소가 로컬 주소인지 확인

        Args:
            client_ip: 확인할 IP 주소

        Returns:
            로컬 IP인 경우 True, 그렇지 않으면 False
        """
        if not client_ip:
            return False

        if client_ip.startswith("127.") or client_ip.startswith("192"):
            return True

        # 172.16.0.0 ~ 172.31.255.255 (172.16/12) 대역 확인
        if client_ip.startswith("172."):
            try:
                parts = client_ip.split(".")
                if len(parts) >= 2:
                    second_octet = int(parts[1])
                    if 16 <= second_octet <= 31:
                        return True
            except (ValueError, IndexError):
                pass

        # 기본 로컬 IP 확인
        if client_ip in self.ALLOWED_LOCAL_IPS:
            return True

        return False

    def _get_client_ip(self, request: Request) -> str | None:
        """
        클라이언트 IP 주소를 추출

        프록시나 로드밸런서 환경을 고려하여 X-Forwarded-For 헤더도 확인

        Args:
            request: Starlette Request 객체

        Returns:
            클라이언트 IP 주소 또는 None
        """
        # X-Forwarded-For 헤더 확인 (프록시 환경 고려)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # 여러 프록시를 거친 경우 첫 번째 IP가 실제 클라이언트 IP
            return forwarded_for.split(",")[0].strip()

        # 직접 연결인 경우
        if request.client:
            return request.client.host

        return None

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        미들웨어 로직 실행

        Args:
            request: Starlette Request 객체
            call_next: 다음 미들웨어 또는 라우트 핸들러를 호출하는 함수

        Returns:
            JSONResponse: 외부 IP 접근 시 403 응답
            또는 다음 미들웨어/핸들러의 응답
        """
        client_ip = self._get_client_ip(request)

        if not self._is_local_ip(client_ip):
            logger.warning(f"외부 IP 접근 차단: {client_ip} - Path: {request.url.path}")
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Forbidden: 외부 접근이 허용되지 않습니다. 로컬 접근만 가능합니다."
                },
            )

        # 로컬 IP인 경우 다음 미들웨어/핸들러로 진행
        response = await call_next(request)
        return response
