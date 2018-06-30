"""
Provides access to the settings file.
"""
try: import simplejson as json
except ImportError: import json
import pathlib
from os import path
from pprint import pprint
from gnucash_portfolio.lib import fileutils

class Settings:
    """Provides access to user settings from settings.json file."""
    def __init__(self, config=None):
        self.FILENAME = "settings.json"
        # Content of the settings.json file. JSON object.
        self.data = config

        if not config:
            self.__load_settings()

    def __load_settings(self):
        """ Load settings from .json file """
        #file_path = path.relpath(settings_file_path)
        #file_path = path.abspath(settings_file_path)
        file_path = self.file_path

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

    def save(self):
        """ Saves the settings contents """
        content = self.dumps()
        fileutils.save_text_to_file(content, self.file_path)

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

    @property
    def favourite_accounts(self):
        """ Favourite accounts. List of account ids. """
        return self.data["favourite_accounts"]

    @property
    def file_path(self) -> str:
        """ Settings file absolute path"""
        file_path = path.abspath(path.join(__file__, "..", "..", "..", "config", self.FILENAME))
        return file_path

    def dumps(self) -> str:
        """ Dumps the json content as a string """
        return json.dumps(self.data, sort_keys=True, indent=4)

    def loads(self, settings: str):
        """ Loads settings from json string """
        self.data = json.loads(settings)

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
