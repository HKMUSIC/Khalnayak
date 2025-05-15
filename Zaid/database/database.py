import datetime
from typing import Optional, List, Any

from motor import motor_asyncio
from motor.core import AgnosticClient
from pymongo.errors import DuplicateKeyError


class Database:
    def __init__(self, uri: str, db_name: str = "mydatabase") -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.session = self.db["session"]
        self.stan_users = self.db["stan_users"]

    async def ensure_indexes(self) -> None:
        """Create necessary indexes for collections."""
        await self.session.create_index("user_id", unique=True)
        await self.stan_users.create_index([("client", 1), ("user_id", 1)], unique=True)

    def get_datetime(self) -> str:
        """Return current UTC datetime string in ISO 8601 format."""
        return datetime.datetime.utcnow().isoformat()

    async def is_stan(self, client: int, user_id: int) -> bool:
        """Check if user is in stan_users."""
        return await self.stan_users.find_one({"client": client, "user_id": user_id}) is not None

    async def add_stan(self, client: int, user_id: int) -> bool:
        """Add a stan user, return False if already exists."""
        if await self.is_stan(client, user_id):
            return False
        try:
            await self.stan_users.insert_one(
                {"client": client, "user_id": user_id, "date": self.get_datetime()}
            )
            return True
        except DuplicateKeyError:
            return False

    async def rm_stan(self, client: int, user_id: int) -> bool:
        """Remove a stan user, return True if deleted."""
        result = await self.stan_users.delete_one({"client": client, "user_id": user_id})
        return result.deleted_count > 0

    async def get_stans(self, client: int) -> List[dict[str, Any]]:
        """Return list of stan users for a client."""
        return [doc async for doc in self.stan_users.find({"client": client})]

    async def get_all_stans(self) -> List[dict[str, Any]]:
        """Return list of all stan users."""
        return [doc async for doc in self.stan_users.find({})]

    async def is_session(self, user_id: int) -> bool:
        """Check if session exists for a user."""
        return await self.session.find_one({"user_id": user_id}) is not None

    async def update_session(self, user_id: int, session: str) -> bool:
        """Update or insert a session. Returns True if operation succeeded."""
        result = await self.session.update_one(
            {"user_id": user_id},
            {"$set": {"session": session, "date": self.get_datetime()}},
            upsert=True,
        )
        return result.acknowledged

    async def rm_session(self, user_id: int) -> bool:
        """Remove a session. Returns True if deleted."""
        result = await self.session.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    async def get_session(self, user_id: int) -> Optional[dict[str, Any]]:
        """Get session info for a user."""
        return await self.session.find_one({"user_id": user_id})

    async def get_all_sessions(self) -> List[dict[str, Any]]:
        """Get all sessions."""
        return [doc async for doc in self.session.find({})]

    def close(self) -> None:
        """Close the MongoDB client."""
        self.client.close()

    def __repr__(self) -> str:
        return f"<Database connected={self.client is not None}>"
