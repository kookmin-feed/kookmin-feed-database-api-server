from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config.db_config import DBManager

app = FastAPI()
db_manager = DBManager()


class DirectMessage(BaseModel):
    user_id: str
    user_name: str
    scrapers: list


class ServerChannel(BaseModel):
    server_id: str
    server_name: str
    channel_id: str
    channel_name: str
    scrapers: list


@app.get("/direct-messages/")
def read_direct_messages_list():
    return db_manager.read_direct_messages_list()


@app.post("/direct-messages/")
def create_direct_message(dm: DirectMessage):
    if db_manager.create_direct_message(dm.user_id, dm.user_name, dm.scrapers):
        return {"message": "Direct message created successfully"}
    raise HTTPException(status_code=500, detail="Failed to create direct message")


@app.get("/direct-messages/{user_id}")
def read_direct_message(user_id: str):
    dm = db_manager.read_direct_message(user_id)
    if dm:
        return dm
    raise HTTPException(status_code=404, detail="Direct message not found")


@app.put("/direct-messages/{user_id}")
def update_direct_message(user_id: str, scrapers: list):
    if db_manager.update_direct_message(user_id, scrapers):
        return {"message": "Direct message updated successfully"}
    raise HTTPException(status_code=500, detail="Failed to update direct message")


@app.delete("/direct-messages/{user_id}")
def delete_direct_message(user_id: str):
    if db_manager.delete_direct_message(user_id):
        return {"message": "Direct message deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete direct message")


@app.get("/server-channels/")
def read_server_channels_list():
    return db_manager.read_server_channels_list()


@app.post("/server-channels/")
def create_server_channel(sc: ServerChannel):
    if db_manager.create_server_channel(
        sc.server_id, sc.server_name, sc.channel_id, sc.channel_name, sc.scrapers
    ):
        return {"message": "Server channel created successfully"}
    raise HTTPException(status_code=500, detail="Failed to create server channel")


@app.get("/server-channels/{server_id}")
def read_server_channel(server_id: str):
    sc = db_manager.read_server_channel(server_id)
    if sc:
        return sc
    raise HTTPException(status_code=404, detail="Server channel not found")


@app.put("/server-channels/{server_id}")
def update_server_channel(server_id: str, scrapers: list):
    if db_manager.update_server_channel(server_id, scrapers):
        return {"message": "Server channel updated successfully"}
    raise HTTPException(status_code=500, detail="Failed to update server channel")


@app.delete("/server-channels/{server_id}")
def delete_server_channel(server_id: str):
    if db_manager.delete_server_channel(server_id):
        return {"message": "Server channel deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete server channel")


@app.get("/notices/{notice_type}")
def read_notice_list(notice_type: str):
    return db_manager.read_notice_list(notice_type)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

