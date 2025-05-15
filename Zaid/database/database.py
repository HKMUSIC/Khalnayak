from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, uri, db_name="SessionDB"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["sessions"]

    async def update_session(self, user_id: int, session_string: str):
        """Add or update a session string for a user."""
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"session_string": session_string}},
            upsert=True
        )

    async def get_session(self, user_id: int):
        """Retrieve a session string for a user."""
        doc = await self.collection.find_one({"user_id": user_id})
        return doc["session_string"] if doc else None

    async def get_all_sessions(self):
        """Get all user session records."""
        sessions = []
        async for doc in self.collection.find():
            sessions.append({
                "user_id": doc["user_id"],
                "session_string": doc["session_string"]
            })
        return sessions

    async def rm_session(self, user_id: int):
        """Remove a session by user ID."""
        result = await self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
