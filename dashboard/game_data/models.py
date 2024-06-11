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
    name = models.CharField(max_length=255)
    center_x = models.IntegerField()
    center_y = models.IntegerField()
    size = models.IntegerField()

    def __str__(self):
        return self.name
# game_data/models.py

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
    required_class = models.ForeignKey(ClassType, on_delete=models.SET_NULL, null=True, blank=True)
    required_level = models.IntegerField(null=True, blank=True)
    commoner_purchase = models.BooleanField(default=False)
    town_purchase = models.BooleanField(default=False)

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

    def __str__(self):
        return self.type

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

    def __str__(self):
        return self.get_name_display()

class Worker(models.Model):
    name = models.CharField(max_length=255)
    work_capacity = models.IntegerField(choices=[(15, '15'), (25, '25')])
    current_building = models.ForeignKey('dashboard.Building', on_delete=models.SET_NULL, null=True, blank=True)
    current_transport = models.ForeignKey('dashboard.Transport', on_delete=models.SET_NULL, null=True, blank=True)
    is_head_of_household = models.BooleanField(default=False)
    current_duty = models.ForeignKey(HouseholdDuty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkerClassLevel(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.worker.name} - {self.class_type.name} - {self.level.name}"


class GamePlayer(models.Model):
    nickname = models.CharField(max_length=255, null=True, blank=True)
    head_of_household = models.OneToOneField('Worker', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_household_for')
    town = models.ForeignKey('Town', on_delete=models.SET_NULL, null=True, blank=True)
    leaderboard_position = models.IntegerField(null=True, blank=True)
    workers = models.ManyToManyField('Worker', blank=True)
    rushes = models.IntegerField(default=3)  # Add this field to track rushes

    def __str__(self):
        return self.nickname

class Contract(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    project = models.CharField(max_length=255)
    items = models.ManyToManyField('Item', through='ContractItem')
    requirement = models.CharField(max_length=255)
    deadline = models.DateField()
    deadline_turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    obligations = models.CharField(max_length=255)
    reward = models.IntegerField()
    assigned_player = models.ForeignKey(GamePlayer, on_delete=models.SET_NULL, null=True, blank=True)

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

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class PlayerSustenance(models.Model):
    player = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
    item = models.ForeignKey(SustenanceItem, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.player.game_player.nickname} - {self.item.name} ({self.quantity})"
