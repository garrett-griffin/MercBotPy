import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from webapp.app import app, get_production_chains

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('webapp.app.get_production_chains')
def test_index(mock_get_production_chains, client: FlaskClient):
    mock_get_production_chains.return_value = [
        ('user1', '{"chain1": [{"building_id": 1, "size": 10, "target": 50}]}'),
        ('user2', '{"chain2": [{"building_id": 2, "size": 5, "target": 30}]}')
    ]
    response = client.get('/')
    assert response.status_code == 200
    assert b'user1' in response.data
    assert b'chain1' in response.data
    assert b'user2' in response.data
    assert b'chain2' in response.data
