from fastapi import APIRouter, HTTPException, Header, Depends
from api.deps import get_api_key, get_db_manager
from config.db_config import DBManager
import os

router = APIRouter()

@router.get(
    "/types",
    summary="스크래퍼 유형 목록 조회",
    description="사용 가능한 스크래퍼 유형 목록을 조회합니다.",
    tags=["Scraper"],
    responses={
        200: {"description": "스크래퍼 유형 목록 조회 성공"},
        403: {"description": "인증 실패"}
    }
)
async def get_scraper_types(
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.read_scraper_type_list()

@router.get(
    "/categories",
    summary="스크래퍼 카테고리 목록 조회",
    description="사용 가능한 스크래퍼 카테고리 목록을 조회합니다.",
    tags=["Scraper"],
    responses={
        200: {"description": "스크래퍼 카테고리 목록 조회 성공"},
        403: {"description": "인증 실패"}
    }
)
async def get_scraper_categories(
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.read_category_list()

