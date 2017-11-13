"""
GnuCash database operations
"""
from lib import settings
import piecash

# Use the settings file.
config = settings.load_settings()
filename = config["gnucash.database"]

#class Database:
#def __init__(self):
    #self.data = []

def open_book():
    """Opens the database"""
    #book = piecash.open_book(filename, open_if_lock=True)
    book = create_book()
    return book

def create_book():
    """Creates a new in-memory book"""
    #piecash.create_book(filename)
    return piecash.create_book()
