""" GnuCash database operations """

import os
from os import path
from logging import log, INFO, WARN
import urllib
import piecash
from gnucash_portfolio.lib.settings import Settings


class Database:
    """ Provides access to the GnuCash book. """

    def __init__(self, db_path: str = None):
        # database file path
        if db_path:
            self.filename = db_path
        else:
            # Use the settings file if no url passed.
            self.__settings = None
            self.filename = self.__config.database_path

    @property
    def __config(self):
        """ settings instance """
        if not self.__settings:
            self.__settings = Settings()

        return self.__settings

    def display_db_info(self):
        """Displays some basic info about the GnuCash book"""
        with self.open_book() as book:
            default_currency = book.default_currency
            print("Default currency is ", default_currency.mnemonic)

    def open_book(self, for_writing=False) -> piecash.Book:
        """
        Opens the database. Call this using 'with'.
        If database file is not found, an in-memory database will be created.
        """
        filename = None

        # check if the file path is already a URL.
        file_url = urllib.parse.urlparse(self.filename)
        if file_url.scheme == "file" or file_url.scheme == "sqlite":
            filename = file_url.path[1:]
        else:
            filename = self.filename

        if not os.path.isfile(filename):
            log(WARN, "Database %s requested but not found. Creating an in-memory book.", filename)
            return self.create_book()

        access_type = "read/write" if for_writing else "readonly"
        log(INFO, "Using %s in %s mode.", filename, access_type)
        # file_path = path.relpath(self.filename)
        file_path = path.abspath(filename)

        if not for_writing:
            book = piecash.open_book(file_path, open_if_lock=True)
        else:
            book = piecash.open_book(file_path, open_if_lock=True, readonly=False)
        # book = create_book()
        return book

    def create_book(self):
        """Creates a new in-memory book"""
        # piecash.create_book(filename)
        return piecash.create_book()


############################################################
def test():
    """ test method """
    database = Database()
    database.display_db_info()

    with database.open_book() as test_book:
        print(test_book.default_currency)


# If run directly, just display some diagnostics data.
if __name__ == "__main__":
    test()
