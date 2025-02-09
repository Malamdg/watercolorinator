import json
import os

# Path to config file
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config/config.json")


def _load_config():
    """load config from `config.json`."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found.")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class Config:
    """Centralized config handling of application."""

    def __init__(self):
        self.config = _load_config()

    def get(self, key, default=None):
        """Get config value using point separator."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default
        return value if value else default


# Singleton : Unique instance of `Config` used in all the app
config = Config()
