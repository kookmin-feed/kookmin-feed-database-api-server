from fastapi import FastAPI, HTTPException, Header, Query
import os
from api.v1.api import api_router
from config.db_config import DBManager
import logging

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

db_manager = DBManager()

API_KEY = os.getenv("API_KEY")


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 8000)
    uvicorn.run("main:app", host=host, port=port, reload=True)