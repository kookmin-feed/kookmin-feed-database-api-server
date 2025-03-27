import logging
from pymongo import MongoClient
from config.env_loader import ENV

logger = logging.getLogger(__name__)

IS_PROD = ENV["IS_PROD"]


class DBManager:
    def __init__(self):
        pass

    def get_database(self, db_name: str = None):
        """MongoDB 데이터베이스 연결을 반환합니다.

        Args:
            db_name (str, optional): 사용할 데이터베이스 이름.
                미지정시 환경변수의 DB_NAME 또는 기본값 사용
        """
        try:
            client = MongoClient(ENV["MONGODB_URI"])
            default_db = "dev-kookmin-feed" if not IS_PROD else "kookmin-feed"
            db_name = db_name or ENV["DB_NAME"] or default_db
            return client[db_name]
        except Exception as e:
            logger.error(f"DB 연결 중 오류 발생: {e}")
            raise

    def get_collection(self, db_name: str = None, collection_name: str = None):
        """DB내 컬렉션 반환."""
        collection = self.get_database(db_name)[collection_name]
        return collection

    def read_direct_messages_list(self):
        """DM 리스트 반환"""
        documents = self.get_collection("notification-recipient", "direct-messages").find()
        doc_list = []
        for doc in documents:
            doc_list.append(doc)
        return doc_list

    def read_server_channels_list(self):
        """채팅 서버 리스트 반환"""
        documents = self.get_collection("notification-recipient", "server-channels").find()
        doc_list = []
        for doc in documents:
            doc_list.append(doc)
        return doc_list

    def create_direct_message(self, user_id: str, user_name: str, scrapers: list):
        """DM 생성"""
        try:
            self.get_database("notification-recipient")["direct-messages"].insert_one(
                {
                    "_id": user_id,
                    "user_name": user_name,
                    "channel_type": "direct-messages",
                    "scrapers": scrapers,
                }
            )
            logger.info(f"DM 정보 생성 완료: {user_name}")
            return True
        except Exception as e:
            logger.error(f"DM 생성 중 오류 발생: {e}")
            return False

    def read_direct_message(self, user_id: str):
        """DM 조회"""
        try:
            document = self.get_database("notification-recipient")["direct-messages"].find_one(
                {"_id": user_id}
            )
            return document
        except Exception as e:
            logger.error(f"DM 조회 중 오류 발생: {e}")
            return None

    def update_direct_message(self, user_id: str, scrapers: list):
        """DM 정보 업데이트"""
        try:
            self.get_database("notification-recipient")["direct-messages"].update_one(
                {"_id": user_id}, {"$set": {"scrapers": scrapers}}
            )
            logger.info(f"DM 정보 업데이트 완료: {user_id}")
            return True
        except Exception as e:
            logger.error(f"DM 정보 업데이트 중 오류 발생: {e}")
            return False

    def delete_direct_message(self, user_id: str):
        """DM 삭제"""
        try:
            self.get_database("notification-recipient")["direct-messages"].delete_one(
                {"_id": user_id}
            )
            logger.info(f"DM 삭제 완료: {user_id}")
            return True
        except Exception as e:
            logger.error(f"DM 삭제 중 오류 발생: {e}")
            return False

    def create_server_channel(
        self,
        server_id: str,
        server_name: str,
        channel_id: str,
        channel_name: str,
        scrapers: list,
    ):
        """채팅 서버 생성"""
        try:
            self.get_database("notification-recipient")["server-channels"].insert_one(
                {
                    "_id": server_id,
                    "server_name": server_name,
                    "channel_id": channel_id,
                    "channel_name": channel_name,
                    "channel_type": "server-channels",
                    "scrapers": scrapers,
                }
            )
            logger.info(f"채팅 서버 정보 생성 완료: {server_name}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 생성 중 오류 발생: {e}")
            return False

    def read_server_channel(self, server_id: str):
        """채팅 서버 조회"""
        try:
            document = self.get_database("notification-recipient")["server-channels"].find_one(
                {"_id": server_id}
            )
            return document
        except Exception as e:
            logger.error(f"채팅 서버 조회 중 오류 발생: {e}")
            return None

    def update_server_channel(self, server_id: str, scrapers: list):
        """채팅 서버 정보 업데이트"""
        try:
            self.get_database("notification-recipient")["server-channels"].update_one(
                {"_id": server_id}, {"$set": {"scrapers": scrapers}}
            )
            logger.info(f"채팅 서버 정보 업데이트 완료: {server_id}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 정보 업데이트 중 오류 발생: {e}")
            return False

    def delete_server_channel(self, server_id: str):
        """채팅 서버 삭제"""
        try:
            self.get_database("notification-recipient")["server-channels"].delete_one(
                {"_id": server_id}
            )
            logger.info(f"채팅 서버 삭제 완료: {server_id}")
            return True
        except Exception as e:
            logger.error(f"채팅 서버 삭제 중 오류 발생: {e}")
            return False

    def read_notice_list(self, notice_type: str = None, list_size: int = 5):
        """공지사항 리스트 반환"""
        documents = self.get_collection(collection_name=notice_type).find(sort=[("published", -1)]).limit(list_size)
        doc_list = []
        for doc in documents:
            dic = {}
            for k, v in doc.items():  # .items()로 수정하여 키-값 쌍을 순회
                if k == "_id": 
                    continue
                dic[k] = v
            doc_list.append(dic)
        return doc_list

    def close_database(self):
        """데이터베이스 연결을 종료합니다."""
        try:
            client = MongoClient(ENV["MONGODB_URI"])
            client.close()
        except Exception as e:
            logger.error(f"DB 연결 종료 중 오류 발생: {e}")

