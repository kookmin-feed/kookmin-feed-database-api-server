import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config.env_loader import ENV
from bson import ObjectId

logger = logging.getLogger(__name__)

IS_PROD = ENV["IS_PROD"]

def transform_object_id(document):
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document

class DBManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(ENV["MONGODB_URI"])
        default_db = "dev-kookmin-feed" if not IS_PROD else "kookmin-feed"
        self.db_name = ENV.get("DB_NAME", default_db)

    async def get_database(self, db_name: str = None):
        return self.client[db_name or self.db_name]

    async def get_collection(self, db_name: str = None, collection_name: str = None):
        return (await self.get_database(db_name))[collection_name]

    async def read_direct_messages_list(self):
        collection = await self.get_collection("notification-recipient", "direct-messages")
        documents = await collection.find().to_list(None)
        return [transform_object_id(doc) for doc in documents]

    async def read_server_channels_list(self):
        collection = await self.get_collection("notification-recipient", "server-channels")
        documents = await collection.find().to_list(None)
        return [transform_object_id(doc) for doc in documents]

    async def create_direct_message(self, user_id: str, user_name: str, scrapers: list):
        try:
            collection = await self.get_collection("notification-recipient", "direct-messages")
            await collection.insert_one({
                "_id": user_id,
                "user_name": user_name,
                "channel_type": "direct-messages",
                "scrapers": scrapers,
            })
            logger.info(f"DM 정보 생성 완료: {user_name}")
            return True
        except Exception as e:
            logger.error(f"DM 생성 중 오류 발생: {e}")
            return False

    async def read_direct_message(self, user_id: str):
        collection = await self.get_collection("notification-recipient", "direct-messages")
        document = await collection.find_one({"_id": user_id})
        return transform_object_id(document)

    async def update_direct_message(self, user_id: str, scrapers: list):
        try:
            collection = await self.get_collection("notification-recipient", "direct-messages")
            await collection.update_one({"_id": user_id}, {"$set": {"scrapers": scrapers}})
            logger.info(f"DM 정보 업데이트 완료: {user_id}")
            return True
        except Exception as e:
            logger.error(f"DM 정보 업데이트 중 오류 발생: {e}")
            return False

    async def delete_direct_message(self, user_id: str):
        try:
            collection = await self.get_collection("notification-recipient", "direct-messages")
            await collection.delete_one({"_id": user_id})
            logger.info(f"DM 삭제 완료: {user_id}")
            return True
        except Exception as e:
            logger.error(f"DM 삭제 중 오류 발생: {e}")
            return False

    async def create_server_channel(self, guild_name: str, channel_id: str, channel_name: str, scrapers: list):
        try:
            collection = await self.get_collection("notification-recipient", "server-channels")
            await collection.insert_one({
                "_id": channel_id,
                "channel_name": channel_name,
                "channel_type": "server-channels",
                "guild_name": guild_name,
                "scrapers": scrapers,
            })
            logger.info(f"채팅 서버 정보 생성 완료: {guild_name}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 생성 중 오류 발생: {e}")
            return False

    async def read_server_channel(self, channel_id: str):
        try:
            collection = await self.get_collection("notification-recipient", "server-channels")
            document = await collection.find_one({"_id": channel_id})
            return transform_object_id(document)
        except Exception as e:
            logger.error(f"채팅 서버 조회 중 오류 발생: {e}")
            return None

    async def update_server_channel(self, channel_id: str, scrapers: list):
        try:
            collection = await self.get_collection("notification-recipient", "server-channels")
            await collection.update_one({"_id": channel_id}, {"$set": {"scrapers": scrapers}})
            logger.info(f"채팅 서버 정보 업데이트 완료: {channel_id}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 정보 업데이트 중 오류 발생: {e}")
            return False

    async def delete_server_channel(self, channel_id: str):
        try:
            collection = await self.get_collection("notification-recipient", "server-channels")
            await collection.delete_one({"_id": channel_id})
            logger.info(f"채팅 서버 삭제 완료: {channel_id}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 삭제 중 오류 발생: {e}")
            return False

    async def read_notice_list(self, notice_type: str = None, list_size: int = 5):
        collection = await self.get_collection(collection_name=notice_type)
        documents = await collection.find().sort([("published", -1), ("_id", -1)]).limit(list_size).to_list(None)
        return [transform_object_id(doc) for doc in documents]

    async def read_category_list(self):
        collection = await self.get_collection("scraper-metadata", "scraper-categories")
        documents = await collection.find().to_list(None)
        return [transform_object_id(doc) for doc in documents]

    async def read_scraper_type_list(self):
        collection = await self.get_collection("scraper-metadata", "scraper-types")
        documents = await collection.find().to_list(None)
        return [transform_object_id(doc) for doc in documents]

    async def close_database(self):
        self.client.close()