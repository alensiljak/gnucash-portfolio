#!/usr/bin/python3
"""
Provides access to the settings file.
"""
try: import simplejson as json 
except ImportError: import json
import pathlib
from os import path
from pprint import pprint

FILENAME = "settings.json"

class Settings:
    """Provides access to user settings from settings.json file."""

    def __init__(self, config=None):
        # Content of the settings.json file. JSON object.
        self.data = config

        if not config:
            self.__load_settings()


    def __load_settings(self):
        """ Load settings from .json file """
        #file_path = path.relpath(settings_file_path)
        #file_path = path.abspath(settings_file_path)
        file_path = path.abspath(path.join(__file__, "..", "..", "..", "config", FILENAME))
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
        Full database path. Includes the default location + the database filename.
        """
        filename = self.database_filename
        db_path = ":memory:" if filename == ":memory:" else (
            path.abspath(path.join(__file__, "../..", "..", "data", filename)))
        return db_path

    @property
    def database_filename(self):
        """ Database file name only. This is the setting value in .json. """
        self.__check_if_data_loaded()

        return self.data["gnucash.database"]


    def __check_if_data_loaded(self):
        """ Checks if the settings file has been loaded and throws an exception if not """
        if not self.data:
            raise FileNotFoundError()

##################################################################
def test():
    """ test from console """
    config = Settings()
    config.show_settings()

# If run directly, just display the settings file.
if __name__ == "__main__":
    test()
