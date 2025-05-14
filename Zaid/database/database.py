import sqlite3

def init_db():
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER PRIMARY KEY,
            session TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_session(user_id: int, session: str):
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("REPLACE INTO sessions (user_id, session) VALUES (?, ?)", (user_id, session))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("SELECT user_id, session FROM sessions")
    sessions = c.fetchall()
    conn.close()
    return sessions
