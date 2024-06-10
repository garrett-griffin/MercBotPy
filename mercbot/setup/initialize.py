import os
import json
import asyncio
from pymerc.game.player import Player
from mercbot.utils.client import load_clients
from mercbot.models.settings import save_settings
from dotenv import load_dotenv

async def initialize_settings(api_nicknames, api_user, api_token):
    load_dotenv()
    nicknames = json.loads(api_nicknames)
    clients = load_clients(api_user, api_token, api_nicknames)

    for nickname in nicknames:
        client = clients[nickname]
        player = Player(client)
        await player.load()

        production_chains = {}
        for building in player.buildings:
            if building.production:
                recipe = str(building.production.recipe)  # Convert recipe to string
                if recipe not in production_chains:
                    production_chains[recipe] = []
                production_chains[recipe].append({
                    "building_id": building.id,
                    "size": building.size,
                    "target": building.production.target
                })

        save_settings(nickname, production_chains)
        print(f"Settings for {nickname} initialized and saved to database.")

if __name__ == "__main__":
    load_dotenv()
    api_user = os.getenv("BOT_USER")
    api_token = os.getenv("BOT_TOKEN")
    api_nicknames = os.getenv("BOT_NICKNAMES")

    api_user = api_user
    api_token = api_token
    api_nicknames = api_nicknames

    asyncio.run(initialize_settings(api_nicknames, api_user, api_token))
