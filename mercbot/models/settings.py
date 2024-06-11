import json
from .database import get_connection

async def save_setting(user_id, setting_key, setting_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO settings (user_id, setting_key, setting_value) VALUES (?, ?, ?)", 
                   (user_id, setting_key, setting_value))
    conn.commit()
    conn.close()

def load_settings(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT setting_key, setting_value FROM settings WHERE user_id = ?", (user_id,))
    result = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in result}

def save_default_settings(user_id):
    default_settings = {
        "allow_writes": "1",
        "allow_production": "1",
        "allow_market": "1",
        "allow_resources": "1"
    }
    conn = get_connection()
    cursor = conn.cursor()
    for key, value in default_settings.items():
        cursor.execute("INSERT INTO settings (user_id, setting_key, setting_value) VALUES (?, ?, ?)", 
                       (user_id, key, value))
    conn.commit()
    conn.close()
