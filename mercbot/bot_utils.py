# bot_utils.py
import asyncio
import os
import json
from pymerc.api.models.common import Item
from pymerc.game.player import Player
from pymerc.client import Client

async def produce_item(player: Player, item_name: str, quantity: int):
    print(f"Producing {quantity} of {item_name}")
    for building in player.buildings:
        if building.production:
            recipe = building.production.recipe
            for output_item in recipe.outputs:
                if output_item.item.name == item_name:
                    target_production = quantity // output_item.quantity
                    print(f"Setting target production for {building.type} to {target_production}")
                    building.production.target = target_production
                    await building.save_production()
                    break

async def balance_item(player: Player, item_name: str, min_stock: int, sell_extras: bool):
    for item, asset in player.storehouse.data.inventory.items.items():
        if item.name == item_name:
            balance = asset.balance
            capacity = asset.capacity
            unit_cost = asset.unit_cost

            print(f"Balancing {item_name}: Balance = {balance}, Capacity = {capacity}, Unit Cost = {unit_cost}")

            # Buy more if stock is below minimum
            if balance < min_stock:
                buy_volume = min_stock - balance
                print(f"Buying {buy_volume} of {item_name}")
                await player.storehouse.data.buy(item, buy_volume, unit_cost)

            # Sell extras if stock is above minimum and sell_extras is True
            if sell_extras and balance > min_stock:
                sell_volume = balance - min_stock
                print(f"Selling {sell_volume} of {item_name}")
                await player.storehouse.data.sell(item, sell_volume, unit_cost)

async def initialize_production_chains(player: Player):
    production_chains = []
    for building in player.buildings:
        if building.production:
            recipe = building.production.recipe
            for output_item in recipe.outputs:
                production_chains.append((output_item.item.name, 100))  # Default quantity, can be adjusted
    return production_chains

def load_clients(api_user, api_token, nicknames):
    clients = {}
    for nickname in nicknames:
        client = Client(api_user, api_token)
        clients[nickname] = client
    return clients

def load_settings():
    with open('bot_settings.json', 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open('bot_settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

async def update_settings_with_production_chains(player: Player, settings):
    production_chains = await initialize_production_chains(player)
    settings['production_chains'] = production_chains
    save_settings(settings)

async def update_settings_with_inventory(player: Player, settings):
    inventory = {}
    for item, asset in player.storehouse.data.inventory.items.items():
        inventory[item.name] = {
            'balance': asset.balance,
            'capacity': asset.capacity,
            'unit_cost': asset.unit_cost
        }
    settings['inventory'] = inventory
    save_settings(settings)
