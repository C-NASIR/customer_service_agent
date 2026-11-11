import json

from src.db import get_db


def load_conversation(conversation_id):
    with get_db() as db:
        row = db.execute("SELECT history, context FROM conversations WHERE id = ?", 
            (conversation_id,)).fetchone()
    
    if not row: return [], []
    return json.loads(row[0]), json.loads(row[1])

def save_conversations(conversation_id, history, context):
    with get_db() as db:
        db.execute("""
            INSERT INTO conversations (id, history, context)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET 
            history = excluded.history, 
            context = excluded.context
        """, (conversation_id, json.dumps(history), json.dumps(context)))