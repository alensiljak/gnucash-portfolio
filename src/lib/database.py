#!/usr/bin/python3
"""
GnuCash database operations
"""
from lib import settings
import piecash
import os
from os import path

class Database:
    config = None
    filename = None   # database file path

    def __init__(self):
        # Use the settings file.
        self.config = settings.Settings()
        self.filename = self.config.data["gnucash.database"]

    def display_db_info(self):
        """Displays some basic info about the GnuCash book"""
        with self.open_book() as book:
            default_currency = book.default_currency
            print("Default currency is ", default_currency.mnemonic)

    def open_book(self, for_writing=False):
        """
        Opens the database. Call this using 'with'. 
        If database file is not found, an in-memory database will be created.
        """
        if not os.path.isfile(self.filename):
            print("Creating an in-memory book.")
            return self.create_book()

        print("Opening " + self.filename)
        file_path = path.relpath(self.filename)

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