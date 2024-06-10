import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '../../data/bot_settings.json')

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
