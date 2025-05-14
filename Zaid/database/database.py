import aiosqlite
import asyncio

DB_PATH = "sessions.db"
TABLE_NAME = "sessions"

def init_db():
    """Initializes the sessions database."""
    asyncio.get_event_loop().run_until_complete(_init_db_async())

async def _init_db_async():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id INTEGER PRIMARY KEY,
                session TEXT NOT NULL
            )
        """)
        await db.commit()

def save_session(user_id: int, session_string: str):
    """Saves or updates a user's session string."""
    asyncio.get_event_loop().run_until_complete(_save_session_async(user_id, session_string))

async def _save_session_async(user_id: int, session_string: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            INSERT INTO {TABLE_NAME} (user_id, session)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET session=excluded.session
        """, (user_id, session_string))
        await db.commit()

def get_all_sessions():
    """Fetches all stored sessions as (user_id, session) tuples."""
    return asyncio.get_event_loop().run_until_complete(_get_all_sessions_async())

async def _get_all_sessions_async():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(f"SELECT user_id, session FROM {TABLE_NAME}") as cursor:
            return await cursor.fetchall()

def remove_session(user_id: int):
    """Removes a user's session by user ID."""
    return asyncio.get_event_loop().run_until_complete(_remove_session_async(user_id))

async def _remove_session_async(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"DELETE FROM {TABLE_NAME} WHERE user_id = ?", (user_id,))
        await db.commit()
