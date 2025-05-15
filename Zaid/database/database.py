from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, uri, db_name="sessionDB"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db.sessions

    async def update_session(self, user_id: int, session_string: str):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"session_string": session_string}},
            upsert=True
        )

    async def get_session(self, user_id: int):
        session = await self.collection.find_one({"user_id": user_id})
        return session["session_string"] if session else None

    async def get_all_sessions(self):
        sessions = []
        async for session in self.collection.find():
            sessions.append({"user_id": session["user_id"], "session_string": session["session_string"]})
        return sessions

    async def rm_session(self, user_id: int):
        result = await self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
