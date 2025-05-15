from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, mongo_url: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client["SessionDB"]
        self.collection = self.db["sessions"]

    async def update_session(self, user_id: int, session_string: str) -> bool:
        """Add or update session for a user."""
        try:
            await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "session_string": session_string}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"[DB ERROR] update_session: {e}")
            return False

    async def rm_session(self, user_id: int) -> bool:
        """Remove session by user ID."""
        try:
            result = await self.collection.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"[DB ERROR] rm_session: {e}")
            return False

    async def get_all_sessions(self) -> list:
        """Return all stored sessions."""
        try:
            sessions = await self.collection.find({}).to_list(length=1000)
            return sessions
        except Exception as e:
            print(f"[DB ERROR] get_all_sessions: {e}")
            return []

    async def get_session(self, user_id: int) -> dict:
        """Return session for a specific user."""
        try:
            return await self.collection.find_one({"user_id": user_id})
        except Exception as e:
            print(f"[DB ERROR] get_session: {e}")
            return None
