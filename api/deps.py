from functools import lru_cache
from fastapi import Header, HTTPException
from config.db_config import DBManager
import os

API_KEY = os.getenv("API_KEY")

@lru_cache()  # 싱글톤 패턴
def get_db_manager():
    """데이터베이스 매니저 싱글톤 인스턴스 반환"""
    return DBManager()

def get_api_key(authorization: str = Header(None, description="Bearer 토큰 형식의 API 키")):
    """API 키 검증"""
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return authorization