import json

from src.db import get_db


def load_conversation(conversation_id):
    with get_db() as db:
        row = db.execute("SELECT history FROM conversations WHERE id = ?", 
            (conversation_id,)).fetchone()
    
    return json.loads(row[0]) if row else []

def save_conversations(conversation_id, history):
    with get_db() as db:
        db.execute("""
            INSERT INTO conversations (id, history)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET history = excluded.history
        """, (conversation_id, json.dumps(history)))