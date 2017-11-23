#!/usr/bin/python3
"""
Provides access to the settings file.
"""
import json
import pathlib
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

        #file_path = path.relpath(settings_file_path)
        #file_path = path.abspath(settings_file_path)
        file_path = path.abspath(path.join(__file__, "..", "..", FILENAME))
        try:
            self.data = json.load(open(file_path))
        except FileNotFoundError:
            print("Could not load", file_path)

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
        """Returns the base currency setting"""
        return self.data["baseCurrency"]

    @property
    def database_uri(self):
        """
        Returns the book database path as URI that can be used for opening
        the book as sql database.
        """
        return pathlib.Path(self.database_path).as_uri()

    @property
    def database_path(self):
        """
        The database path.
        """
        filename = self.database_filename
        db_path = path.abspath(path.join(__file__, "..", "..", "data", filename))
        return db_path

    @property
    def database_filename(self):
        return self.data["gnucash.database"]

# If run directly, just display the settings file.
if __name__ == "__main__":
    config = Settings()
    config.show_settings()
