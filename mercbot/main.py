import asyncio
import os
import json
from dotenv import load_dotenv
from mercbot.utils.client import load_clients
from mercbot.models.settings import load_settings_to_db
from mercbot.utils.production import optimize_production, manage_resources
from mercbot.utils.market import analyze_market

async def main():
    load_dotenv()
    api_user = os.getenv("BOT_USER")
    api_token = os.getenv("BOT_TOKEN")
    api_nicknames = os.getenv("BOT_NICKNAMES")

    nicknames = json.loads(api_nicknames)
    clients = load_clients(api_user, api_token, api_nicknames)

    for nickname in nicknames:
        client = clients[nickname]
        player = Player(client)
        await player.load()

        # Load settings from the database
        settings = load_settings_to_db(nickname)

        # Optimize production
        await optimize_production(player)

        # Analyze market and determine pricing strategy
        pricing_strategy = await analyze_market(player)
        print(f"Pricing Strategy for {nickname}: {pricing_strategy}")

        # Manage resources
        for item_name in settings["items"]:
            await manage_resources(player, item_name, settings["items"][item_name]["min_stock"], settings["items"][item_name]["sell_extras"])

if __name__ == "__main__":
    asyncio.run(main())
