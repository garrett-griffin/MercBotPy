from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_user = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null=True, blank=True)

class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setting_key = models.CharField(max_length=255)
    setting_value = models.TextField()