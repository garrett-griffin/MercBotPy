import os
import json
import asyncio
from pymerc.game.player import Player
from mercbot.utils.client import load_clients
from mercbot.utils.production import update_production_chains
from dotenv import load_dotenv

async def initialize_settings(api_nicknames, api_user, api_token):
    load_dotenv()

    if not api_nicknames.startswith('['):
        api_nicknames = f'["{api_nicknames}"]'

    nicknames = json.loads(api_nicknames)
    clients = load_clients(api_user, api_token, api_nicknames)

    for nickname in nicknames:
        client = clients[nickname]
        player = Player(client)
        await player.load()

        await update_production_chains(player, nickname)

if __name__ == "__main__":
    load_dotenv()
    api_user = os.getenv("BOT_USER")
    api_token = os.getenv("BOT_TOKEN")
    api_nicknames = os.getenv("BOT_NICKNAMES")

    api_user = api_user
    api_token = api_token
    api_nicknames = api_nicknames

    asyncio.run(initialize_settings(api_nicknames, api_user, api_token))
