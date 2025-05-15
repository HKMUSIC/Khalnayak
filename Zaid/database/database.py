from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client.program  # Database name
collection = db.sessions  # Collection name for session storage

async def init_db():
    """
    Initializes the sessions collection by ensuring a unique index on user_id.
    MongoDB automatically creates the collection if it doesn't exist.
    """
    await collection.create_index("user_id", unique=True)

async def save_session(user_id: int, session_string: str):
    """
    Saves or updates a session string for a given user_id.
    If the user already exists, it updates the session.
    """
    await collection.update_one(
        {"user_id": user_id},
        {"$set": {"session": session_string}},
        upsert=True
    )

async def get_all_sessions():
    """
    Returns all stored (user_id, session_string) tuples.
    """
    sessions = []
    async for document in collection.find({}):
        sessions.append((document["user_id"], document["session"]))
    return sessions

async def remove_session(user_id: int):
    """
    Deletes the session entry for the specified user_id.
    """
    await collection.delete_one({"user_id": user_id})
