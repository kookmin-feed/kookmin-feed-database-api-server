from fastapi import APIRouter, Depends
from api.deps import get_api_key

router = APIRouter()

@router.get(
    "/connect-check",
    summary="연결 상태 확인",
    description="API 서버의 연결 상태를 확인합니다.",
    tags=["Health Check"],
    responses={
        200: {"description": "연결 성공"},
        403: {"description": "인증 실패"}
    }
)
async def checking_connection(_: str = Depends(get_api_key)):
    return "200 OK"