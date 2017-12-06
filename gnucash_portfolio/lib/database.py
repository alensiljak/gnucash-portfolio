#!/usr/bin/python3
"""
GnuCash database operations
"""
import os
from os import path
#import pathlib
import urllib
import piecash
from .settings import Settings

class Database:
    """
    Provides access to the GnuCash book.
    """
    config = None
    filename = None   # database file path

    def __init__(self, book_url: str = None):
        # Use the settings file.
        self.config = Settings()
        if not book_url:
            self.filename = self.config.database_path
        
        self.filename = book_url


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

        if not os.path.isfile(filename):
            print("Creating an in-memory book.")
            return self.create_book()

        print("Using", filename)
        #file_path = path.relpath(self.filename)
        file_path = path.abspath(filename)

        if not for_writing:
            book = piecash.open_book(file_path, open_if_lock=True)
        else:
            book = piecash.open_book(file_path, open_if_lock=True, readonly=False)
        #book = create_book()
        return book


    def create_book(self):
        """Creates a new in-memory book"""
        #piecash.create_book(filename)
        return piecash.create_book()

# If run directly, just display some diagnostics data.
if __name__ == "__main__":
    db = Database()
    db.display_db_info()

    with db.open_book() as test_book:
        print(test_book.default_currency)
