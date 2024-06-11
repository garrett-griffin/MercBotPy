import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/mercbot.db')

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        api_user TEXT NOT NULL,
        api_token TEXT NOT NULL,
        nickname TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        setting_key TEXT NOT NULL,
        setting_value TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    # Assuming we have a default user with id 1 for demonstration purposes
    default_user_id = 1
    save_default_settings(default_user_id)
    print("Database initialized successfully.")
