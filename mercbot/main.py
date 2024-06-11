import asyncio
import os
import json
from dotenv import load_dotenv
from mercbot.utils.client import load_clients
from mercbot.models.settings import load_settings_to_db
from mercbot.utils.production import optimize_production, manage_resources
from mercbot.utils.market import fetch_market_data, analyze_market
from pymerc.game.player import Player

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

        if not settings["allow_writes"]:
            print(f"Writes are disabled for {nickname}. Skipping...")
            continue

        # Optimize production
        if settings["allow_production"]:
            await optimize_production(player)

        # Ensure town data is loaded before fetching market data
        await player.town.load()

        # Fetch market data
        if settings["allow_market"]:
            market_data = await fetch_market_data(player)
            # Analyze market and determine pricing strategy
            pricing_strategy = analyze_market(market_data)
            print(f"Pricing Strategy for {nickname}: {pricing_strategy}")

        # Manage resources
        if settings["allow_resources"]:
            if settings["production_chains"] is not None:
                for item_name in settings["production_chains"]["items"]:
                    await manage_resources(player, item_name, settings["production_chains"]["items"][item_name]["min_stock"], settings["production_chains"]["items"][item_name]["sell_extras"])

if __name__ == "__main__":
    asyncio.run(main())
