from django.db import models
from django.contrib.auth.models import User
# dashboard/models.py

from game_data.models import GamePlayer, BuildingType, TransportType

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    game_player = models.OneToOneField(GamePlayer, on_delete=models.CASCADE, null=True, blank=True)
    api_user = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)


class Building(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    production_capacity = models.IntegerField()
    building_type = models.ForeignKey(BuildingType, on_delete=models.CASCADE)

class Transport(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    capacity = models.IntegerField()

class BuildingGroup(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    buildings = models.ManyToManyField(Building)

class ProductionChain(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sequence_order = models.IntegerField()
    buildings = models.ManyToManyField(Building, blank=True)
    building_groups = models.ManyToManyField(BuildingGroup, blank=True)

class Action(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    turn_number = models.IntegerField()
    action_type = models.CharField(max_length=255)
    details = models.TextField()

class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)  # New field
    setting_key = models.CharField(max_length=255)
    setting_value = models.TextField()

class TileAttribute(models.Model):
    name = models.CharField(max_length=255)

class TileTax(models.Model):
    attribute = models.ForeignKey(TileAttribute, on_delete=models.CASCADE)
    tax_amount = models.FloatField()

class BuildingType(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.IntegerField()
    production_capacity = models.IntegerField()
    build_location = models.CharField(max_length=255)
    required_tile_attributes = models.ManyToManyField(TileAttribute, blank=True)