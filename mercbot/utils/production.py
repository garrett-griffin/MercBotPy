from pymerc.game.player import Player
from mercbot.models.settings import save_settings_to_db

async def identify_production_chains(player: Player):
    production_chains = {}

    for building in player.buildings:
        if building.production:
            recipe = str(building.production.recipe)  # Convert recipe to string
            target = building.production.target or 0  # Ensure target is an integer
            if recipe not in production_chains:
                production_chains[recipe] = []
            production_chains[recipe].append({
                "building_id": building.id,
                "size": building.size,
                "target": target
            })

    return production_chains

def calculate_efficiency(production_chain):
    efficiency = 0
    for step in production_chain:
        efficiency += step["target"]  # Simplistic calculation
    return efficiency

def prioritize_chains(chains):
    prioritized = sorted(chains.items(), key=lambda x: calculate_efficiency(x[1]), reverse=True)
    return prioritized

async def optimize_production(player):
    chains = await identify_production_chains(player)
    prioritized_chains = prioritize_chains(chains)
    # Implement logic to adjust production based on prioritized chains
    for recipe, chain in prioritized_chains:
        print(f"Optimizing production for {recipe} with chain: {chain}")
        # Adjust production targets as needed

async def update_production_chains(player: Player, nickname: str):
    print("Entering update_production_chains")
    production_chains = await identify_production_chains(player)
    print(f"Identified production chains: {production_chains}")
    try:
        print(f"save_settings_to_db about to be called")
        await save_settings_to_db(nickname, production_chains)  # Ensure this is awaited
        print(f"save_settings_to_db called with: {nickname}, {production_chains}")
        print(f"Production chains for {nickname} updated and saved to database.")
    except Exception as e:
        print(f"Exception in save_settings: {e}")

async def produce_item(player: Player, item_name: str, amount: int, settings: dict):
    for recipe, buildings in settings.items():
        if item_name.lower() in recipe.lower():
            for building in buildings:
                building_id = building['building_id']
                target = amount  # Adjust based on logic
                print(f"Setting production target for {item_name} in building {building_id} to {target}")
                # await player.update_production_target(building_id, target)
            break
    else:
        print(f"No production chain found for {item_name}")

async def balance_item(player: Player, item_name: str, min_stock: int = 50, sell_extras: bool = True):
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
                await player.storehouse.buy(item, buy_volume, unit_cost)

            # Sell extras if stock is above minimum and sell_extras is True
            if sell_extras and balance > min_stock:
                sell_volume = balance - min_stock
                print(f"Selling {sell_volume} of {item_name}")
                await player.storehouse.sell(item, sell_volume, unit_cost)

async def manage_resources(player, item_name, min_stock=50, sell_extras=True):
    for item, asset in player.storehouse.data.inventory.items.items():
        if item.name == item_name:
            balance = asset.balance
            capacity = asset.capacity
            unit_cost = asset.unit_cost

            # Buy more if stock is below minimum
            if balance < min_stock:
                buy_volume = min_stock - balance
                # await player.storehouse.data.buy(item, buy_volume, unit_cost)

            # Sell extras if stock is above minimum and sell_extras is True
            if sell_extras and balance > min_stock:
                sell_volume = balance - min_stock
                # await player.storehouse.data.sell(item, sell_volume, unit_cost)
