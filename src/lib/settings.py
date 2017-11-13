"""
Provides access to the settings file.
"""
import json
from os import path
from pprint import pprint

FILENAME = "../settings.json"

class Settings:
    """Provides access to user settings from settings.json file."""
    data = None

    def __init__(self, file_path):
        if not file_path:
            file_path = FILENAME
        
        file_path = path.relpath(file_path)
        self.data = json.load(open(file_path))
        return

    # def get_default_currency():
    #     return self.data[]

    def show_settings(self):
        """Displays the contents of the settings file"""
        self.data = self.load_settings()
        pprint(self.data)

    def load_settings(self):
        """Returns the settings JSON from the file"""
        return self.data

    def get_rates(self):
        """Returns the list of exchange rates from the settings"""
        self.data = self.load_settings()
        return self.data["exchangeRates"]

    def get_currencies(self):
        """Fetches the list of currencies from the settings."""
        self.data = self.load_settings()
        return self.data["currencies"]

# If run directly, just display the settings file.
if __name__ == "__main__":
    config = Settings()
    config.show_settings()
