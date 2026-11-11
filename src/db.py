import sqlite3
from contextlib import contextmanager

DATABASE = "customer_service_agent_database.db"


def db_init():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY, 
                history TEXT NOT NULL,
                context TEXT NOT NULL
            )
        """)


@contextmanager
def get_db():
    db = sqlite3.connect(DATABASE)

    try:
        with db:
            yield db 
    finally:
        db.close()
