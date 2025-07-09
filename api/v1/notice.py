from fastapi import APIRouter, HTTPException, Header, Query, Depends
from api.deps import get_api_key, get_db_manager
from config.db_config import DBManager
from typing import Optional
import os

router = APIRouter()

@router.get(
    "/all",
    summary="공지사항 목록 조회",
    description="공지사항 목록을 조회합니다.",
    tags=["Notices"],
    responses={
        200: {"description": "공지사항 목록 조회 성공"},
        403: {"description": "인증 실패"}
    }
)
async def get_notices(
    notice_type: str,
    list_size: int = 10,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.read_notice_list(notice_type, list_size)

@router.get(
    "/new",
    summary="새로운 공지사항 조회",
    description="마지막 확인 이후의 새로운 공지사항을 조회합니다.",
    tags=["Notices"],
    responses={
        200: {"description": "새로운 공지사항 조회 성공"},
        403: {"description": "인증 실패"}
    }
)
async def get_new_notice(
    notice_type: str,
    last_notice_link: str,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    notices = await db_manager.read_notice_list(notice_type, 50)
    response_list = []

    for notice in notices:
        if notice.get("link") == last_notice_link:
            break
        response_list.append(notice)
    
    return response_list

