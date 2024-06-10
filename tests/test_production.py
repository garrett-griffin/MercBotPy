import pytest
from unittest.mock import AsyncMock, patch, ANY
from mercbot.utils.production import balance_item, produce_item, identify_production_chains, update_production_chains
from mercbot.models.database import initialize_database
from pymerc.api.models.common import Item
from pymerc.game.player import Player
import mercbot.models.settings


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


class MockBuilding:
    def __init__(self, id, production, size):
        self.id = id
        self.production = production
        self.size = size  # Add the size attribute


class MockProduction:
    def __init__(self, recipe, target):
        self.recipe = recipe
        self.target = target


class MockPlayer:
    def __init__(self, inventory, buildings):
        self.storehouse = MockStorehouse(inventory)
        self.buildings = buildings
        self.update_production_target = AsyncMock()


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    initialize_database()


@pytest.fixture
def mock_player():
    inventory = {
        Item.Rope: MockAsset(balance=30, capacity=100, unit_cost=10),
        Item.FlaxPlants: MockAsset(balance=70, capacity=100, unit_cost=5),
        Item.FlaxFibres: MockAsset(balance=50, capacity=100, unit_cost=7)
    }
    buildings = [
        MockBuilding(1, MockProduction("rope production", 50), 10),
        MockBuilding(2, MockProduction("flax production", 30), 5)
    ]
    player = MockPlayer(inventory, buildings)
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


@pytest.mark.asyncio
async def test_identify_production_chains(mock_player):
    production_chains = await identify_production_chains(mock_player)
    assert "rope production" in production_chains
    assert len(production_chains["rope production"]) == 1
    assert production_chains["rope production"][0]["building_id"] == 1


@pytest.mark.asyncio
@patch('mercbot.utils.production.save_settings_to_db', new_callable=AsyncMock)
async def test_update_production_chains(mock_save_settings_to_db, mock_player):
    print(f"Patch path: {'mercbot.utils.production.save_settings_to_db'}")
    print(f"Mocked save_settings_to_db: {mock_save_settings_to_db}")

    nickname = "test_nickname"

    # Call the function that uses save_settings_to_db
    await update_production_chains(mock_player, nickname)

    # Add debug statement to ensure the function call
    print(f"save_settings_to_db call count: {mock_save_settings_to_db.call_count}")

    try:
        mock_save_settings_to_db.assert_called_once_with(nickname, {'rope production': ANY, 'flax production': ANY})
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
        print(f"save_settings_to_db call args: {mock_save_settings_to_db.call_args_list}")
        raise e


@pytest.mark.asyncio
@patch('mercbot.utils.production.save_settings_to_db', new_callable=AsyncMock)
async def test_full_update_production_chains(mock_save_settings_to_db, mock_player):
    print(f"Patch path: {'mercbot.utils.production.save_settings_to_db'}")
    print(f"Mocked save_settings_to_db: {mock_save_settings_to_db}")

    nickname = "test_nickname"
    await update_production_chains(mock_player, nickname)

    # Add debug statement to ensure the function call
    print(f"save_settings_to_db call count: {mock_save_settings_to_db.call_count}")

    try:
        mock_save_settings_to_db.assert_called_once_with(nickname, {'rope production': ANY, 'flax production': ANY})
    except AssertionError as e:
        print(f"AssertionError: {str(e)}")
        print(f"save_settings_to_db call args: {mock_save_settings_to_db.call_args_list}")
        raise e
