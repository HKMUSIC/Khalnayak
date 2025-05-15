from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, uri):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client["StrangerBot"]
        self.sessions = self.db.sessions

    async def update_session(self, user_id, session_str):
        await self.sessions.update_one(
            {"user_id": user_id},
            {"$set": {"session_string": session_str, "user_id": user_id}},
            upsert=True
        )

    async def get_all_sessions(self):
        return await self.sessions.find().to_list(length=None)

    async def rm_session(self, user_id):
        result = await self.sessions.delete_one({"user_id": user_id})
        return result.deleted_count > 0
