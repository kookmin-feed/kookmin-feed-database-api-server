from pydantic import BaseModel
from typing import List

class DirectMessageCreate(BaseModel):
    user_id: str
    user_name: str
    scrapers: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "user_name": "JohnDoe",
                "scrapers": ["scraper1", "scraper2"]
            }
        }

class DirectMessageUpdate(BaseModel):
    user_id: str
    scrapers: List[str]

class ServerChannelCreate(BaseModel):
    guild_name: str
    channel_id: str
    channel_name: str
    scrapers: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "guild_name": "TestServer",
                "channel_id": "channel123",
                "channel_name": "General",
                "scrapers": ["scraper1"]
            }
        }

class ServerChannelUpdate(BaseModel):
    channel_id: str
    scrapers: List[str]