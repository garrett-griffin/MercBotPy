import json
from pymerc.client import Client
from mercbot.models.database import get_connection

def load_clients(api_user: str, api_token: str, api_nicknames: str) -> dict:
    clients = {}

    if not api_user.startswith("["):
        api_user = f'["{api_user}"]'

    if not api_token.startswith("["):
        api_token = f'["{api_token}"]'

    if not api_user.startswith("[") or not api_token.startswith("["):
        raise ValueError("Invalid API user or token")

    users = json.loads(api_user)
    tokens = json.loads(api_token)
    nicknames = json.loads(api_nicknames)

    if len(users) != len(tokens) or len(users) != len(nicknames):
        raise ValueError("Mismatch in the number of users, tokens, and nicknames")

    conn = get_connection()
    cursor = conn.cursor()

    for user, token, nickname in zip(users, tokens, nicknames):
        cursor.execute("SELECT id FROM users WHERE username = ?", (user,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            clients[nickname] = Client(user_id, token)
        else:
            raise ValueError(f"User '{user}' does not exist")

    conn.close()

    return clients
