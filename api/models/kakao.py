from pydantic import BaseModel
from typing import List

class KakaoUserCreate(BaseModel):
    user_id: str
    scrapers: List[str]
    access_token: str
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "kakao_user_123",
                "scrapers": ["scraper1", "scraper2"],
                "access_token": "your_access_token_here"
            }
        }

class KakaoUserUpdate(BaseModel):
    user_id: str
    scrapers: List[str]
    access_token: str