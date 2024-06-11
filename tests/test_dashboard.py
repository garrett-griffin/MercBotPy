import os
import pytest

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

import django

# Initialize Django
django.setup()

from django.urls import reverse
from django.test import Client
from unittest.mock import patch
from dashboard.frontend.views import get_production_chains

@pytest.fixture
def client():
    return Client()

@patch('dashboard.frontend.views.get_production_chains')
def test_index(mock_get_production_chains, client):
    mock_get_production_chains.return_value = [
        ('user1', '{"chain1": [{"building_id": 1, "size": 10, "target": 50}]}'),
        ('user2', '{"chain2": [{"building_id": 2, "size": 5, "target": 30}]}')
    ]
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b'user1' in response.content
    assert b'chain1' in response.content
    assert b'user2' in response.content
    assert b'chain2' in response.content
