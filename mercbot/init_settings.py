# init_settings.py
import sqlite3
import os
import json
import asyncio
from pymerc.client import Client
from pymerc.game.player import Player
from dotenv import load_dotenv

load_dotenv()

def load_clients(api_user, api_token, nicknames):
    clients = {}
    for nickname in nicknames:
        client = Client(api_user, api_token)
        clients[nickname] = client
    return clients

async def determine_production_chains(player):
    production_chains = []
    for building in player.buildings:
        if building.production:
            recipe = building.production.recipe
            for output_item in recipe.outputs:
                production_chains.append((output_item.item, 100))  # Set default quantity to 100, adjust as needed
    return production_chains

async def initialize_settings(nickname, api_user, api_token):
    client = Client(api_user, api_token)
    player = Player(client)
    await player.load()

    conn = sqlite3.connect('mercatorio.db')
    cursor = conn.cursor()

    # Insert account settings
    cursor.execute('''
    INSERT OR IGNORE INTO account_settings (nickname, api_user, api_token)
    VALUES (?, ?, ?)
    ''', (nickname, api_user, api_token))

    cursor.execute('SELECT id FROM account_settings WHERE nickname=?', (nickname,))
    account_id = cursor.fetchone()[0]

    # Determine production chains automatically
    production_chains = await determine_production_chains(player)
    for item, quantity in production_chains:
        cursor.execute('''
        INSERT OR IGNORE INTO production_chain (account_id, item, quantity)
        VALUES (?, ?, ?)
        ''', (account_id, item, quantity))

    # Initialize balance items (for example, rope and nets)
    balance_items = [
        ('Rope', 50, True),
        ('Net', 50, True)
    ]

    for item, min_stock, sell_extras in balance_items:
        cursor.execute('''
        INSERT OR IGNORE INTO balance_items (account_id, item, min_stock, sell_extras)
        VALUES (?, ?, ?)
        ''', (account_id, item, min_stock, sell_extras))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    api_user = json.loads(os.getenv("BOT_USER"))[0]
    api_token = json.loads(os.getenv("BOT_TOKEN"))[0]
    nicknames = json.loads(os.getenv("BOT_NICKNAMES"))
    for nickname in nicknames:
        asyncio.run(initialize_settings(nickname, api_user, api_token))
