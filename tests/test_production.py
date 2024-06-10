import pytest
from unittest.mock import AsyncMock
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

class MockStorehouseData:
    def __init__(self, inventory):
        self.inventory = inventory

class MockStorehouse:
    def __init__(self, inventory):
        self.data = MockStorehouseData(MockInventory(inventory))
        self.buy = AsyncMock()
        self.sell = AsyncMock()

class MockPlayer:
    def __init__(self, inventory):
        self.storehouse = MockStorehouse(inventory)
        self.update_production_target = AsyncMock()

@pytest.fixture
def mock_player():
    inventory = {
        Item.Rope: MockAsset(balance=30, capacity=100, unit_cost=10),
        Item.FlaxPlants: MockAsset(balance=70, capacity=100, unit_cost=5),
        Item.FlaxFibres: MockAsset(balance=50, capacity=100, unit_cost=7)
    }
    player = MockPlayer(inventory)
    return player

@pytest.mark.asyncio
async def test_balance_item(mock_player):
    await balance_item(mock_player, "Rope", min_stock=50, sell_extras=True)
    await balance_item(mock_player, "FlaxPlants", min_stock=50, sell_extras=True)
    await balance_item(mock_player, "FlaxFibres", min_stock=100, sell_extras=False)

    # Verify that the buy and sell methods were called with expected arguments
    mock_player.storehouse.buy.assert_any_call(Item.Rope, 20, 10)
    mock_player.storehouse.sell.assert_any_call(Item.FlaxPlants, 20, 5)
    mock_player.storehouse.buy.assert_any_call(Item.FlaxFibres, 50, 7)

@pytest.mark.asyncio
async def test_produce_item(mock_player, capfd):
    item_name = "Rope"
    quantity = 100
    settings = {
        "rope production": [
            {"building_id": 1, "size": 10, "target": 50}
        ]
    }
    await produce_item(mock_player, item_name, quantity, settings)

    # Capture the printed output
    captured = capfd.readouterr()
    assert "Setting production target for Rope in building 1 to 100" in captured.out
