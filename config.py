import json
import os


class Config:
    """Centralized configuration loader."""

    CONFIG_FILE = "config/config.json"

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        """Load the configuration from a JSON file."""
        if not os.path.exists(self.CONFIG_FILE):
            raise FileNotFoundError(f"Configuration file {self.CONFIG_FILE} not found.")

        with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key, default=None):
        """Retrieve a value from the configuration using dot notation."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value else default


# Singleton instance of the configuration
config = Config()
