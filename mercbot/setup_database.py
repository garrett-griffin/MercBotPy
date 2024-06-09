# setup_database.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('mercatorio.db')
    cursor = conn.cursor()

    # Create tables for settings and production chains
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS account_settings (
        id INTEGER PRIMARY KEY,
        nickname TEXT UNIQUE,
        api_user TEXT,
        api_token TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS production_chain (
        id INTEGER PRIMARY KEY,
        account_id INTEGER,
        item TEXT,
        quantity INTEGER,
        FOREIGN KEY(account_id) REFERENCES account_settings(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance_items (
        id INTEGER PRIMARY KEY,
        account_id INTEGER,
        item TEXT,
        min_stock INTEGER,
        sell_extras BOOLEAN,
        FOREIGN KEY(account_id) REFERENCES account_settings(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
