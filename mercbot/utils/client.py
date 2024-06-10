import json
from pymerc.client import Client

def load_clients(api_user: str, api_token: str, api_nicknames: str) -> dict:
    clients = {}

    if not api_user.startswith("[") and not api_token.startswith("["):
        api_user = "[" + api_user + "]"
        api_token = "[" + api_token + "]"

    if not api_user.startswith("[") or not api_token.startswith("["):
        raise ValueError("Invalid API user or token")

    users = json.loads(api_user)
    tokens = json.loads(api_token)
    nicknames = json.loads(api_nicknames)

    if len(users) != len(tokens) or len(users) != len(nicknames):
        raise ValueError("Mismatch in the number of users, tokens, and nicknames")

    for user, token, nickname in zip(users, tokens, nicknames):
        clients[nickname] = Client(user, token)

    return clients
