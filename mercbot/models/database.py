import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/mercbot.db')

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL,
        production_chains TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
