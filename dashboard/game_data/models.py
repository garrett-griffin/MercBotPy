from django.db import models

class Turn(models.Model):
    turn_number = models.IntegerField()
    month = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"Turn {self.turn_number}: {self.month} {self.year}"

class Sync(models.Model):
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    turn_number = models.IntegerField()
    timestamp = models.DateTimeField()
    records = models.IntegerField()

    def __str__(self):
        return f"Sync {self.turn} - {self.timestamp}"

class Region(models.Model):
    id = models.IntegerField(primary_key=True)  # Ensure id is stored correctly
    name = models.CharField(max_length=255)
    center_x = models.IntegerField()
    center_y = models.IntegerField()
    size = models.IntegerField()

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=255)
    location_x = models.IntegerField()
    location_y = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    capital = models.BooleanField(default=False)
    commoners = models.IntegerField()
    gentry = models.IntegerField()
    district = models.IntegerField()
    structures = models.IntegerField()
    total_taxes = models.IntegerField()
    climate = models.CharField(max_length=10, choices=[('cold', 'Cold'), ('warm', 'Warm')], default='warm')
    growth_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PrestigeBonus(models.Model):
    PRESTIGE_LABELS = [
        ('common', 'Common'),
        ('established', 'Established'),
        ('reputable', 'Reputable'),
        ('distinguished', 'Distinguished'),
        ('exalted', 'Exalted'),
        ('legend', 'Legend'),
    ]

    level = models.IntegerField()
    label = models.CharField(max_length=20, choices=PRESTIGE_LABELS)
    description = models.CharField(max_length=255)
    tenants_bonus = models.IntegerField(default=0)
    total_tenants = models.IntegerField(default=0)
    luxury_consumption_bonus = models.IntegerField(default=0)
    total_luxury_consumption = models.IntegerField(default=0)
    apprentice_bonus = models.IntegerField(default=0)
    total_apprentices = models.IntegerField(default=0)
    building_capacity_bonus = models.IntegerField(default=0)
    total_building_capacity = models.IntegerField(default=0)
    transport_capacity_bonus = models.IntegerField(default=0)
    total_transport_capacity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.label} ({self.level}): {self.description}"


class ClassType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ClassLevel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    access = models.TextField()
    details = models.TextField()

    def __str__(self):
        return self.name

class ConstructionRequirement(models.Model):
    turn_counter = models.IntegerField()
    items = models.ManyToManyField('Item', through='ConstructionRequirementItem')

class ConstructionRequirementItem(models.Model):
    construction_requirement = models.ForeignKey(ConstructionRequirement, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Item(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    required_class = models.ForeignKey(ClassType, on_delete=models.SET_NULL, null=True, blank=True, related_name="required_by_items")
    required_level = models.IntegerField(null=True, blank=True)
    commoner_purchase = models.BooleanField(default=False)
    town_purchase = models.BooleanField(default=False)
    weight = models.FloatField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    calories = models.FloatField(null=True, blank=True)
    price_low = models.FloatField(null=True, blank=True)
    price_typical = models.FloatField(null=True, blank=True)
    price_high = models.FloatField(null=True, blank=True)
    classes = models.ManyToManyField(ClassType, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    tier = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class CommonerPurchaseRequest(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()

    def __str__(self):
        return f"{self.town.name} - {self.item.name} ({self.quantity_requested})"

class TownPurchaseRequest(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_requested = models.IntegerField()

    def __str__(self):
        return f"{self.town.name} - {self.item.name} ({self.quantity_requested})"

class TileAttribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TileTax(models.Model):
    attribute = models.ForeignKey(TileAttribute, on_delete=models.CASCADE)
    tax_amount = models.FloatField()

    def __str__(self):
        return f"{self.attribute.name}: {self.tax_amount}d"

class BuildingType(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.IntegerField()
    production_capacity = models.IntegerField()
    build_location = models.CharField(max_length=255)
    required_tile_attributes = models.ManyToManyField('TileAttribute', blank=True)
    construction_requirement = models.OneToOneField(ConstructionRequirement, on_delete=models.CASCADE)
    expansion_discount = models.FloatField(null=True, blank=True)
    classes = models.ManyToManyField('ClassType', blank=True)
    supports_boost = models.BooleanField(default=False)
    upgrades = models.ManyToManyField('BuildingUpgrade', blank=True, related_name='upgraded_by')

    def __str__(self):
        return self.name

class BuildingUpgrade(models.Model):
    name = models.CharField(max_length=255)
    construction_requirement = models.OneToOneField(ConstructionRequirement, on_delete=models.CASCADE)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='required_by')

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    labor_required = models.FloatField()
    required_building_upgrade = models.ForeignKey(BuildingUpgrade, on_delete=models.SET_NULL, null=True, blank=True)
    requires_master_level_worker = models.BooleanField(default=False)
    tier = models.IntegerField(null=True, blank=True)
    building = models.CharField(max_length=255, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    class_field = models.CharField(max_length=255, null=True, blank=True)
    points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeInput(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='inputs', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity} of {self.item_name} for {self.recipe.name}"

class RecipeOutput(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='outputs', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity} of {self.item_name} from {self.recipe.name}"

class TransportType(models.Model):
    type = models.CharField(max_length=255)
    capacity = models.IntegerField()
    category = models.CharField(max_length=255, null=True, blank=True)
    tier = models.IntegerField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    journey_duration = models.FloatField(null=True, blank=True)
    effective_days = models.IntegerField(null=True, blank=True)
    operating_costs = models.ManyToManyField('Item', through='OperatingCost')
    catches = models.CharField(max_length=255, null=True, blank=True)
    fishing_range = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.type

class OperatingCost(models.Model):
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class MarketData(models.Model):
    town = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField()
    last_price = models.FloatField()
    average_price = models.FloatField()
    moving_average = models.FloatField()
    highest_bid = models.FloatField()
    lowest_ask = models.FloatField()
    volume = models.IntegerField()
    volume_prev_12 = models.IntegerField()
    bid_volume_10 = models.IntegerField()
    ask_volume_10 = models.IntegerField()

    def __str__(self):
        return f"{self.item.name} in {self.town}"

class HouseholdDuty(models.Model):
    DUTY_CHOICES = [
        ('delivery_1', 'Delivery Duty 1'),
        ('delivery_2', 'Delivery Duty 2'),
        ('knight_1', 'Knight Duty 1'),
        ('knight_2', 'Knight Duty 2'),
        ('knight_3', 'Knight Duty 3'),
        ('knight_4', 'Knight Duty 4'),
    ]

    name = models.CharField(max_length=255, choices=DUTY_CHOICES)
    duty_cost = models.FloatField(null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name

class Player(models.Model):
    nickname = models.CharField(max_length=255, null=True, blank=True)
    head_of_household = models.OneToOneField('Worker', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_household_for')
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, null=True, blank=True)
    leaderboard_position = models.IntegerField(null=True, blank=True)
    workers = models.ManyToManyField('Worker', blank=True)
    rushes = models.IntegerField(default=3)  # Add this field to track rushes
    prestige = models.FloatField(null=True, blank=True)  # Add this field
    portrait = models.CharField(max_length=255, null=True, blank=True)  # Add this field
    gender = models.CharField(max_length=10, null=True, blank=True)  # Add this field
    caps_transports = models.IntegerField(default=0)  # Add this field
    caps_buildings = models.IntegerField(default=0)  # Add this field
    caps_prestige_buildings = models.IntegerField(default=0)  # Add this field
    caps_farmsteads = models.IntegerField(default=0)  # Add this field
    caps_tenants = models.IntegerField(default=0)  # Add this field
    household_inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, null=True, blank=True, related_name='player_household')

    def __str__(self):
        return self.nickname

class Inventory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    balance = models.FloatField()
    reserved = models.FloatField()
    capacity = models.FloatField(null=True, blank=True)
    unit_cost = models.FloatField(null=True, blank=True)


class Contract(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    project = models.CharField(max_length=255)
    items = models.ManyToManyField('Item', through='ContractItem')
    requirement = models.CharField(max_length=255)
    deadline = models.DateField()
    deadline_turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    obligations = models.CharField(max_length=255)
    reward = models.IntegerField()
    assigned_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.town.name} - {self.project}"

class ContractItem(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.name} for {self.contract.project}"



class SustenanceCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SustenanceItem(models.Model):
    category = models.ForeignKey(SustenanceCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    units_required = models.FloatField()
    prestige_effect = models.FloatField()
    prestige_penalty = models.FloatField(default=0)
    unit_cost = models.FloatField(null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class PlayerSustenance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(SustenanceItem, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.player.nickname} - {self.item.name} ({self.quantity})"

class Route(models.Model):
    game_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=255)
    starting_town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='starting_routes')
    destination_town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='destination_routes')
    number_of_moves = models.IntegerField()
    distance = models.FloatField()
    is_land_route = models.BooleanField(default=True)  # True for land, False for water

    def __str__(self):
        return f"{self.name} ({self.starting_town} to {self.destination_town})"

class RouteStep(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='steps')
    sequence_number = models.IntegerField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()

    class Meta:
        unique_together = ('route', 'sequence_number')
        ordering = ['sequence_number']

    def __str__(self):
        return f"Step {self.sequence_number} for {self.route.name} at ({self.coordinate_x}, {self.coordinate_y})"

class PrestigeImpact(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='prestige_impacts')
    factor = models.CharField(max_length=255)
    impact = models.FloatField()

class Manager(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    max_holding = models.IntegerField(null=True, blank=True)
    buy_volume = models.IntegerField(null=True, blank=True)
    buy_price = models.FloatField(null=True, blank=True)
    sell_volume = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)

class HouseholdCaps(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='caps')
    transports = models.IntegerField()
    buildings = models.IntegerField()
    prestige_buildings = models.IntegerField()
    farmsteads = models.IntegerField()
    tenants = models.IntegerField()

class Building(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    production_capacity = models.IntegerField()
    building_type = models.ForeignKey(BuildingType, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)  # Add this field
    location_x = models.IntegerField(null=True, blank=True)  # Add this field
    location_y = models.IntegerField(null=True, blank=True)  # Add this field
    delivery_cost = models.FloatField(null=True, blank=True)  # Add this field
    delivery_land_distance = models.FloatField(null=True, blank=True)
    capacity = models.FloatField(null=True, blank=True)  # Add this field
    upgrades = models.ManyToManyField(BuildingUpgrade, blank=True)  # Updated field
    limited = models.BooleanField(default=False)  # Add this field
    recipe = models.CharField(max_length=255, null=True, blank=True)  # Add this field
    manager = models.CharField(max_length=255, null=True, blank=True)  # Add this field
    provider_id = models.CharField(max_length=255, null=True, blank=True)  # Add this field
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)

class Tile(models.Model):
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    ask_price = models.FloatField(null=True, blank=True)


class PreviousFlow(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='previous_flows')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    consumption = models.FloatField(null=True, blank=True)

class Transport(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    size = models.IntegerField()
    name = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='current_town')
    hometown = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='hometown')
    location_x = models.IntegerField(null=True, blank=True)
    location_y = models.IntegerField(null=True, blank=True)
    capacity = models.FloatField()
    provider_id = models.CharField(max_length=255, null=True, blank=True)
    route = models.OneToOneField(Route, on_delete=models.CASCADE, null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)


class Worker(models.Model):
    name = models.CharField(max_length=255)
    work_capacity = models.IntegerField(choices=[(15, '15'), (25, '25')])
    current_building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)
    current_transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True)
    is_head_of_household = models.BooleanField(default=False)
    current_duty = models.ForeignKey(HouseholdDuty, on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name


class WorkerClassLevel(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.worker.name} - {self.class_type.name} - {self.level.name}"

class Flow(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='flows', null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='flows', null=True, blank=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='flows', null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='flows')
    consumption = models.FloatField(null=True, blank=True)
    shortfall = models.FloatField(null=True, blank=True)