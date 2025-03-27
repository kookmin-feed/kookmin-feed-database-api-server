from fastapi import FastAPI, HTTPException, Request, Header  # Header 추가
import os  # os 모듈 추가
from pydantic import BaseModel
from config.db_config import DBManager

app = FastAPI(docs_url=None)

db_manager = DBManager()

API_KEY = os.getenv("API_KEY")  # 환경 변수에서 API_KEY 가져오기

def validate_api_key(authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

@app.get("/connect-check")
def checking_connection(authorization: str = Header(None)):
    validate_api_key(authorization)
    try:
        return '200 OK'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/discord/direct-messages")
def get_direct_messages(authorization: str = Header(None)):
    validate_api_key(authorization)
    try:
        return db_manager.read_direct_messages_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/discord/direct-messages")
def create_direct_message(authorization: str = Header(None), dm=None):
    validate_api_key(authorization)
    success = db_manager.create_direct_message(dm.user_id, dm.user_name, dm.scrapers)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create direct message")
    return {"message": "Direct message created successfully"}

@app.get("/discord/direct-messages")
def get_direct_message(authorization: str = Header(None), user_id: str = None):
    validate_api_key(authorization)
    dm = db_manager.read_direct_message(user_id)
    if not dm:
        raise HTTPException(status_code=404, detail="Direct message not found")
    return dm

@app.put("/discord/direct-messages")
def update_direct_message(authorization: str = Header(None), user_id: str = None, scrapers: list = None):
    validate_api_key(authorization)
    success = db_manager.update_direct_message(user_id, scrapers)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update direct message")
    return {"message": "Direct message updated successfully"}

@app.delete("/discord/direct-messages")
def delete_direct_message(authorization: str = Header(None), user_id: str = None):
    validate_api_key(authorization)
    success = db_manager.delete_direct_message(user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete direct message")
    return {"message": "Direct message deleted successfully"}

@app.get("/discord/server-channels")
def get_server_channels(authorization: str = Header(None)):
    validate_api_key(authorization)
    try:
        return db_manager.read_server_channels_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/discord/server-channels")
def create_server_channel(authorization: str = Header(None), sc=None):
    validate_api_key(authorization)
    success = db_manager.create_server_channel(
        sc.server_id, sc.server_name, sc.channel_id, sc.channel_name, sc.scrapers
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create server channel")
    return {"message": "Server channel created successfully"}

@app.get("/discord/server-channels")
def get_server_channel(authorization: str = Header(None), server_id: str = None):
    validate_api_key(authorization)
    sc = db_manager.read_server_channel(server_id)
    if not sc:
        raise HTTPException(status_code=404, detail="Server channel not found")
    return sc

@app.put("/discord/server-channels")
def update_server_channel(authorization: str = Header(None), server_id: str = None, scrapers: list = None):
    validate_api_key(authorization)
    success = db_manager.update_server_channel(server_id, scrapers)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update server channel")
    return {"message": "Server channel updated successfully"}

@app.delete("/discord/server-channels")
def delete_server_channel(authorization: str = Header(None), server_id: str = None):
    validate_api_key(authorization)
    success = db_manager.delete_server_channel(server_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete server channel")
    return {"message": "Server channel deleted successfully"}

@app.get("/notices/all")
def get_notices(authorization: str = Header(None), notice_type: str = None, list_size: int = 10):
    validate_api_key(authorization)
    try:
        return db_manager.read_notice_list(notice_type, list_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notices/new")
def get_new_notice(authorization: str = Header(None), notice_type: str = None, last_notice_link: str = None):
    validate_api_key(authorization)
    notices = db_manager.read_notice_list(notice_type)
    
    ret = []

    for notice in notices:
        if notice["link"] == last_notice_link:
            break
        ret.append(notice)

    return ret

@app.get("/scraper/types")
def get_scraper_types(authorization: str = Header(None)):
    validate_api_key(authorization)
    try:
        return db_manager.read_scraper_type_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scraper/categories")
def get_scraper_categories(authorization: str = Header(None)):
    validate_api_key(authorization)
    try:
        return db_manager.read_category_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

