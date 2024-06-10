import os
import pytest
import sqlite3
import json
from mercbot.setup.initialize import initialize_settings
from mercbot.models.settings import load_settings

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/mercbot.db')

@pytest.fixture
def setup_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    conn = sqlite3.connect(DATABASE_PATH)
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
    yield
    os.remove(DATABASE_PATH)

@pytest.mark.asyncio
async def test_initialize_settings(setup_database):
    api_user = '["test_user"]'
    api_token = '["test_token"]'
    api_nicknames = '["test_nickname"]'

    await initialize_settings(api_nicknames, api_user, api_token)
    settings = load_settings("test_nickname")
    assert settings is not None
    assert isinstance(settings, dict)
