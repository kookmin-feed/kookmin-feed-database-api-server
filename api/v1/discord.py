from fastapi import APIRouter, HTTPException, Depends, Query
from api.deps import get_api_key, get_db_manager
from api.models.discord import DirectMessageCreate, DirectMessageUpdate, ServerChannelCreate, ServerChannelUpdate
from api.models.common import SuccessResponse
from config.db_config import DBManager

router = APIRouter()

@router.get(
    "/direct-messages",
    summary="DM 목록 조회",
    description="모든 Discord Direct Message 설정을 조회합니다.",
    tags=["Discord"]
)
async def get_direct_messages(
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.read_direct_messages_list()

@router.post(
    "/direct-messages",
    summary="DM 생성",
    description="새로운 Discord Direct Message 설정을 생성합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def create_direct_message(
    data: DirectMessageCreate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.create_direct_message(
        data.user_id, data.user_name, data.scrapers
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create direct message")
    return {"message": "Direct message created successfully"}

@router.get(
    "/direct-message",
    summary="특정 DM 조회",
    description="특정 사용자의 Discord Direct Message 설정을 조회합니다.",
    tags=["Discord"]
)
async def get_direct_message(
    user_id: str = Query(..., description="조회할 사용자 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    dm = await db_manager.read_direct_message(user_id)
    if not dm:
        raise HTTPException(status_code=404, detail="Direct message not found")
    return dm

@router.put(
    "/direct-messages",
    summary="DM 수정",
    description="Discord Direct Message 설정을 수정합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def update_direct_message(
    data: DirectMessageUpdate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.update_direct_message(data.user_id, data.scrapers)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update direct message")
    return {"message": "Direct message updated successfully"}

@router.delete(
    "/direct-messages",
    summary="DM 삭제",
    description="Discord Direct Message 설정을 삭제합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def delete_direct_message(
    user_id: str = Query(..., description="삭제할 사용자 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.delete_direct_message(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete direct message")
    return {"message": "Direct message deleted successfully"}

@router.get(
    "/server-channels",
    summary="서버 채널 목록 조회",
    description="모든 Discord Server Channel 설정을 조회합니다.",
    tags=["Discord"]
)
async def get_server_channels(
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.read_server_channels_list()

@router.post(
    "/server-channels",
    summary="서버 채널 생성",
    description="새로운 Discord Server Channel 설정을 생성합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def create_server_channel(
    data: ServerChannelCreate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.create_server_channel(
        guild_name=data.guild_name, 
        channel_id=data.channel_id, 
        channel_name=data.channel_name, 
        scrapers=data.scrapers
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create server channel")
    return {"message": "Server channel created successfully"}

@router.get(
    "/server-channel",
    summary="특정 서버 채널 조회",
    description="특정 Discord Server Channel 설정을 조회합니다.",
    tags=["Discord"]
)
async def get_server_channel(
    channel_id: str,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    sc = await db_manager.read_server_channel(channel_id)
    if not sc:
        raise HTTPException(status_code=404, detail="Server channel not found")
    return sc

@router.put(
    "/server-channels",
    summary="서버 채널 스크래퍼 수정",
    description="Discord Server Channel 스크래퍼를 수정합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def update_server_channel(
    data: ServerChannelUpdate,
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.update_server_channel(data.channel_id, data.scrapers)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update server channel")
    return {"message": "Server channel updated successfully"}

@router.delete(
    "/server-channels",
    summary="서버 채널 삭제",
    description="Discord Server Channel 설정을 삭제합니다.",
    response_model=SuccessResponse,
    tags=["Discord"]
)
async def delete_server_channel(
    channel_id: str = Query(..., description="삭제할 채널 ID"),
    _: str = Depends(get_api_key),
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.delete_server_channel(channel_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete server channel")
    return {"message": "Server channel deleted successfully"}