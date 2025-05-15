import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, mongo_url: str = MONGO_URL):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client["SessionDB"]
        self.collection = self.db["sessions"]
        logger.info("Database connection initialized.")

    async def update_session(self, user_id: int, session_string: str) -> bool:
        try:
            await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "session_string": session_string}},
                upsert=True
            )
            logger.info(f"Session updated for user_id {user_id}")
            return True
        except Exception as e:
            logger.error(f"update_session error: {e}")
            return False

    async def rm_session(self, user_id: int) -> bool:
        try:
            result = await self.collection.delete_one({"user_id": user_id})
            if result.deleted_count > 0:
                logger.info(f"Session removed for user_id {user_id}")
                return True
            logger.warning(f"No session found for user_id {user_id}")
            return False
        except Exception as e:
            logger.error(f"rm_session error: {e}")
            return False

    async def get_all_sessions(self) -> list:
        try:
            sessions = await self.collection.find({}).to_list(length=1000)
            logger.info(f"Fetched {len(sessions)} sessions")
            return sessions
        except Exception as e:
            logger.error(f"get_all_sessions error: {e}")
            return []

    async def get_session(self, user_id: int) -> dict:
        try:
            session = await self.collection.find_one({"user_id": user_id})
            if session:
                logger.info(f"Session fetched for user_id {user_id}")
            else:
                logger.warning(f"No session found for user_id {user_id}")
            return session
        except Exception as e:
            logger.error(f"get_session error: {e}")
            return None

    async def clear_all_sessions(self) -> bool:
        """Remove all sessions from the database."""
        try:
            result = await self.collection.delete_many({})
            logger.info(f"All sessions cleared. Deleted count: {result.deleted_count}")
            return True
        except Exception as e:
            logger.error(f"clear_all_sessions error: {e}")
            return False
