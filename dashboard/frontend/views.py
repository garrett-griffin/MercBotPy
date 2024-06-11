from django.shortcuts import render
from django.http import JsonResponse
import logging

from django.contrib.auth.models import User
from dashboard.models import Account

def get_production_chains():
    return [
        ('user1', '{"chain1": [{"building_id": 1, "size": 10, "target": 50}]}'),
        ('user2', '{"chain2": [{"building_id": 2, "size": 5, "target": 30}]}')
    ]

def index(request):
    chains = get_production_chains()
    logging.info(f"Chains: {chains}")
    return JsonResponse(chains, safe=False)