from django.db import models
from django.contrib.auth.models import User
# dashboard/models.py

from game_data.models import Player, Building

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, null=True, blank=True)
    api_user = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)

class BuildingGroup(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    buildings = models.ManyToManyField(Building)

class ProductionChain(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sequence_order = models.IntegerField()
    buildings = models.ManyToManyField(Building, blank=True)
    building_groups = models.ManyToManyField(BuildingGroup, blank=True)

class Action(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    turn_number = models.IntegerField()
    action_type = models.CharField(max_length=255)
    details = models.TextField()

class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)  # New field
    setting_key = models.CharField(max_length=255)
    setting_value = models.TextField()