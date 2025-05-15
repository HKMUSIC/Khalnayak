import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# MongoDB setup
cli = AsyncIOMotorClient(MONGO_URL)
dbb = cli.program  # database
collection = dbb.sessions  # collection, replacing "sessions" table

async def init_db():
    """MongoDB doesn't require table initialization like SQL, but this can ensure indexes."""
    await collection.create_index("user_id", unique=True)

def save_session(user_id: int, session_string: str):
    """Saves or updates a user's session string."""
    asyncio.get_event_loop().run_until_complete(_save_session_async(user_id, session_string))

async def _save_session_async(user_id: int, session_string: str):
    await collection.update_one(
        {"user_id": user_id},
        {"$set": {"session": session_string}},
        upsert=True
    )

def get_all_sessions():
    """Fetches all stored sessions as (user_id, session) tuples."""
    return asyncio.get_event_loop().run_until_complete(_get_all_sessions_async())

async def _get_all_sessions_async():
    cursor = collection.find({})
    sessions = []
    async for document in cursor:
        sessions.append((document["user_id"], document["session"]))
    return sessions

def remove_session(user_id: int):
    """Removes a user's session by user ID."""
    return asyncio.get_event_loop().run_until_complete(_remove_session_async(user_id))

async def _remove_session_async(user_id: int):
    await collection.delete_one({"user_id": user_id})
