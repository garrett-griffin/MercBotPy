# bot.py
import os
import json
import asyncio
import sqlite3
from pymerc.client import Client
from pymerc.game.player import Player
from bot_utils import produce_item
from dotenv import load_dotenv

async def load_settings(nickname):
    conn = sqlite3.connect('mercatorio.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM account_settings WHERE nickname=?', (nickname,))
    account_settings = cursor.fetchone()

    cursor.execute('SELECT * FROM production_chain WHERE account_id=?', (account_settings[0],))
    production_chain = cursor.fetchall()

    cursor.execute('SELECT * FROM balance_items WHERE account_id=?', (account_settings[0],))
    balance_items = cursor.fetchall()

    conn.close()
    return account_settings, production_chain, balance_items


def load_clients(api_user, api_token, nicknames):
    clients = {}
    for nickname in nicknames:
        client = Client(api_user, api_token)
        clients[nickname] = client
    return clients


async def main():
    load_dotenv()
    api_user = json.loads(os.getenv("BOT_USER"))[0]
    api_token = json.loads(os.getenv("BOT_TOKEN"))[0]
    nicknames = json.loads(os.getenv("BOT_NICKNAMES"))

    clients = load_clients(api_user, api_token, nicknames)

    for nickname in nicknames:
        client = clients[nickname]
        player = Player(client)
        await player.load()

        account_settings, production_chain, balance_items = await load_settings(nickname)

        print(f"Player Name: {player.household.name}")
        print(f"Prestige: {player.prestige}")
        print(f"Money: {player.money}")

        for building in player.buildings:
            print(f"Building ID: {building.id}, Type: {building.type}, Size: {building.size}")
            if building.production:
                print(f"\tRecipe: {building.production.recipe}")
                print(f"\tTarget Production: {building.production.target}")

        print("\nInventory Details:")
        for item, asset in player.storehouse.data.inventory.items.items():
            print(f"{item.name}: Balance = {asset.balance}, Capacity = {asset.capacity}, Unit Cost = {asset.unit_cost}")

        # Produce items based on production_chain
        for item, quantity in production_chain:
            await produce_item(player, item, quantity)

if __name__ == "__main__":
    asyncio.run(main())
