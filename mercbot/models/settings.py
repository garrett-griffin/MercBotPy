import json
from .database import get_connection

def save_settings(nickname, production_chains):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO settings (nickname, production_chains) VALUES (?, ?)", (nickname, json.dumps(production_chains)))
    conn.commit()
    conn.close()

def load_settings(nickname):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT production_chains FROM settings WHERE nickname = ?", (nickname,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return None
