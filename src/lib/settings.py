"""
Provides access to the settings file.
"""
import json
from os import path
from pprint import pprint

#FILENAME = "../settings.json"
FILENAME = "settings.json"

class Settings:
    """Provides access to user settings from settings.json file."""
    data = None

    def __init__(self, settings_file_path=None):
        if not settings_file_path:
            settings_file_path = FILENAME

        file_path = path.relpath(settings_file_path)
        self.data = json.load(open(settings_file_path))

    def show_settings(self):
        """Displays the contents of the settings file"""
        pprint(self.data)

    def get_rates(self):
        """Returns the list of exchange rates from the settings"""
        return self.data["exchangeRates"]

    def get_currencies(self):
        """Fetches the list of currencies from the settings."""
        return self.data["currencies"]

    @property
    def base_currency(self):
        return self.data["baseCurrency"]


# If run directly, just display the settings file.
if __name__ == "__main__":
    config = Settings()
    config.show_settings()
