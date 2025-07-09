from fastapi import APIRouter, HTTPException, Depends, Query
from api.deps import get_api_key, get_db_manager
from api.models.kakao import KakaoUserCreate, KakaoUserUpdate
from api.models.common import SuccessResponse
from config.db_config import DBManager

router = APIRouter()

@router.post(
    "/user",
    summary="카카오 사용자 생성",
    description="새로운 카카오 사용자를 생성합니다.",
    response_model=SuccessResponse,
    tags=["Kakao"],
    responses={
        200: {"description": "카카오 사용자 생성 성공"},
        400: {"description": "잘못된 요청 데이터"},
        403: {"description": "인증 실패"},
        500: {"description": "서버 오류"}
    }
)
async def create_kakao_user(
    data: KakaoUserCreate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    # 추가 비즈니스 로직 검증
    if not data.user_id or not data.user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required and cannot be empty")
    
    if not data.scrapers or len(data.scrapers) == 0:
        raise HTTPException(status_code=400, detail="At least one scraper is required")
    
    if not data.access_token or not data.access_token.strip():
        raise HTTPException(status_code=400, detail="Access token is required and cannot be empty")
    
    success = await db_manager.create_kakao_user(
        data.user_id, data.scrapers, data.access_token
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create kakao user")
    return {"message": "Kakao user created successfully"}

@router.get(
    "/user",
    summary="카카오 사용자 조회",
    description="특정 카카오 사용자 정보를 조회합니다.",
    tags=["Kakao"],
    responses={
        200: {"description": "카카오 사용자 조회 성공"},
        400: {"description": "잘못된 요청 파라미터"},
        403: {"description": "인증 실패"},
        404: {"description": "사용자를 찾을 수 없음"}
    }
)
async def get_kakao_user(
    user_id: str = Query(..., description="조회할 사용자 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required and cannot be empty")
    
    user = await db_manager.read_kakao_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kakao user not found")
    return user

@router.put(
    "/user",
    summary="카카오 사용자 수정",
    description="카카오 사용자 정보를 수정합니다.",
    response_model=SuccessResponse,
    tags=["Kakao"],
    responses={
        200: {"description": "카카오 사용자 수정 성공"},
        400: {"description": "잘못된 요청 데이터"},
        403: {"description": "인증 실패"},
        500: {"description": "서버 오류"}
    }
)
async def update_kakao_user(
    data: KakaoUserUpdate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    # 추가 비즈니스 로직 검증
    if not data.user_id or not data.user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required and cannot be empty")
    
    if not data.scrapers or len(data.scrapers) == 0:
        raise HTTPException(status_code=400, detail="At least one scraper is required")
    
    if not data.access_token or not data.access_token.strip():
        raise HTTPException(status_code=400, detail="Access token is required and cannot be empty")
    
    success = await db_manager.update_kakao_user(data.user_id, data.scrapers, data.access_token)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update kakao user")
    return {"message": "Kakao user updated successfully"}

@router.delete(
    "/user",
    summary="카카오 사용자 삭제",
    description="카카오 사용자를 삭제합니다.",
    response_model=SuccessResponse,
    tags=["Kakao"],
    responses={
        200: {"description": "카카오 사용자 삭제 성공"},
        400: {"description": "잘못된 요청 파라미터"},
        403: {"description": "인증 실패"},
        500: {"description": "서버 오류"}
    }
)
async def delete_kakao_user(
    user_id: str = Query(..., description="삭제할 사용자 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required and cannot be empty")
    
    success = await db_manager.delete_kakao_user(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete kakao user")
    return {"message": "Kakao user deleted successfully"}

@router.get(
    "/token",
    summary="카카오 토큰 조회",
    description="특정 사용자의 카카오 액세스 토큰을 조회합니다.",
    tags=["Kakao"],
    responses={
        200: {"description": "토큰 조회 성공"},
        400: {"description": "잘못된 요청 파라미터"},
        403: {"description": "인증 실패"},
        404: {"description": "사용자 또는 토큰을 찾을 수 없음"}
    }
)
async def get_kakao_token(
    user_id: str = Query(..., description="토큰을 조회할 사용자 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID is required and cannot be empty")
    
    user = await db_manager.read_kakao_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kakao user not found")
    
    if not user.get("access_token"):
        raise HTTPException(status_code=404, detail="Kakao token not found")
    
    return user["access_token"]
