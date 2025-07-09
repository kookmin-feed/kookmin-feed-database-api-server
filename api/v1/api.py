from fastapi import APIRouter
from api.v1 import health, discord, kakao, notice, scraper

api_router = APIRouter()

# 각 도메인별 라우터 등록
api_router.include_router(health.router, tags=["Health Check"])
api_router.include_router(discord.router, prefix="/discord", tags=["Discord"])
api_router.include_router(kakao.router, prefix="/kakao", tags=["Kakao"])
api_router.include_router(notice.router, prefix="/notices", tags=["Notices"])
api_router.include_router(scraper.router, prefix="/scraper", tags=["Scraper"]) 