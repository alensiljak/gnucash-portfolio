"""
GnuCash database operations
"""
from lib import settings
import piecash
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

    def open_book(self):
        """Opens the database. Call this using 'with'."""
        print("Using " + self.filename)
        file_path = path.relpath(self.filename)

        book = piecash.open_book(file_path, open_if_lock=True)
        #book = create_book()
        return book

    def create_book(self):
        """Creates a new in-memory book"""
        #piecash.create_book(filename)
        return piecash.create_book()

# If run directly, just display some diagnostics data.
if __name__ == "__main__":
    Database().display_db_info()