from fastapi import FastAPI, HTTPException, Header
import os
from config.db_config import DBManager
from middleware import LocalAccessMiddleware
import logging

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

# 로컬 접근만 허용하는 미들웨어 추가
app.add_middleware(LocalAccessMiddleware)

db_manager = DBManager()

API_KEY = os.getenv("API_KEY")


def validate_api_key(authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")


@app.get("/connect-check")
async def checking_connection(authorization: str = Header(None)):
    validate_api_key(authorization)
    return "200 OK"


@app.get("/discord/direct-messages")
async def get_direct_messages(authorization: str = Header(None)):
    validate_api_key(authorization)
    return await db_manager.read_direct_messages_list()


@app.post("/discord/direct-messages")
async def create_direct_message(authorization: str = Header(None), data: dict = None):
    validate_api_key(authorization)
    success = await db_manager.create_direct_message(
        data["user_id"], data["user_name"], data["scrapers"]
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create direct message")
    return {"message": "Direct message created successfully"}


@app.get("/discord/direct-message")
async def get_direct_message(authorization: str = Header(None), user_id: str = None):
    validate_api_key(authorization)
    dm = await db_manager.read_direct_message(user_id)
    if not dm:
        raise HTTPException(status_code=404, detail="Direct message not found")
    return dm


@app.put("/discord/direct-messages")
async def update_direct_message(authorization: str = Header(None), data: dict = None):
    validate_api_key(authorization)
    success = await db_manager.update_direct_message(data["user_id"], data["scrapers"])
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update direct message")
    return {"message": "Direct message updated successfully"}


@app.delete("/discord/direct-messages")
async def delete_direct_message(authorization: str = Header(None), user_id: str = None):
    validate_api_key(authorization)
    success = await db_manager.delete_direct_message(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete direct message")
    return {"message": "Direct message deleted successfully"}


@app.get("/discord/server-channels")
async def get_server_channels(authorization: str = Header(None)):
    validate_api_key(authorization)
    return await db_manager.read_server_channels_list()


@app.post("/discord/server-channels")
async def create_server_channel(authorization: str = Header(None), data: dict = None):
    validate_api_key(authorization)
    success = await db_manager.create_server_channel(
        guild_name=data["guild_name"],
        channel_id=data["channel_id"],
        channel_name=data["channel_name"],
        scrapers=data["scrapers"],
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create server channel")
    return {"message": "Server channel created successfully"}


@app.get("/discord/server-channel")
async def get_server_channel(authorization: str = Header(None), channel_id: str = None):
    validate_api_key(authorization)
    sc = await db_manager.read_server_channel(channel_id)
    if not sc:
        raise HTTPException(status_code=404, detail="Server channel not found")
    return sc


@app.put("/discord/server-channels")
async def update_server_channel(authorization: str = Header(None), data: dict = None):
    validate_api_key(authorization)
    success = await db_manager.update_server_channel(
        data["channel_id"], data["scrapers"]
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update server channel")
    return {"message": "Server channel updated successfully"}


@app.delete("/discord/server-channels")
async def delete_server_channel(
    authorization: str = Header(None), channel_id: str = None
):
    validate_api_key(authorization)
    success = await db_manager.delete_server_channel(channel_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete server channel")
    return {"message": "Server channel deleted successfully"}


@app.get("/notices/all")
async def get_notices(
    authorization: str = Header(None), notice_type: str = None, list_size: int = 10
):
    validate_api_key(authorization)
    return await db_manager.read_notice_list(notice_type, list_size)


@app.get("/notices/new")
async def get_new_notice(
    authorization: str = Header(None),
    notice_type: str = None,
    last_notice_link: str = None,
):
    validate_api_key(authorization)
    notices = await db_manager.read_notice_list(notice_type, 50)
    response_list = []

    for notice in notices:
        if notice["link"] == last_notice_link:
            break
        response_list.append(notice)

    return response_list


@app.get("/scraper/types")
async def get_scraper_types(authorization: str = Header(None)):
    validate_api_key(authorization)
    return await db_manager.read_scraper_type_list()


@app.get("/scraper/categories")
async def get_scraper_categories(authorization: str = Header(None)):
    validate_api_key(authorization)
    return await db_manager.read_category_list()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
