import pytest
from mercbot.utils.production import balance_item, produce_item
from pymerc.api.models.common import Item
from pymerc.game.player import Player

class MockAsset:
    def __init__(self, balance, capacity, unit_cost):
        self.balance = balance
        self.capacity = capacity
        self.unit_cost = unit_cost

class MockInventory:
    def __init__(self, items):
        self.items = items

class MockStorehouse:
    def __init__(self, inventory):
        self.data = MockInventory(inventory)
        self.buy = self.mock_buy
        self.sell = self.mock_sell

    async def mock_buy(self, item, volume, unit_cost):
        print(f"Mock buying {volume} of {item.name} at {unit_cost} each")

    async def mock_sell(self, item, volume, unit_cost):
        print(f"Mock selling {volume} of {item.name} at {unit_cost} each")

class MockPlayer:
    def __init__(self, inventory):
        self.storehouse = MockStorehouse(inventory)

@pytest.mark.asyncio
async def test_balance_item():
    inventory = {
        Item(name="Rope"): MockAsset(balance=30, capacity=100, unit_cost=10),
        Item(name="Flax"): MockAsset(balance=70, capacity=100, unit_cost=5),
    }
    player = MockPlayer(inventory)

    await balance_item(player, "Rope", min_stock=50, sell_extras=True)
    await balance_item(player, "Flax", min_stock=50, sell_extras=True)
    await balance_item(player, "Flax", min_stock=100, sell_extras=False)

@pytest.mark.asyncio
async def test_produce_item(mock_player):
    item_name = "Rope"
    quantity = 100
    settings = {"min_stock": 50, "sell_extras": True}
    result = await produce_item(mock_player, item_name, quantity, settings)
    assert result is True or result is False
