"""
GnuCash database operations
"""
import settings
import piecash

# Use the settings file.
#settings.show_settings()
config = settings.load_settings()
filename = config["gnucash.database"]
#print("Working with " + filename)

def open_book():
    """Opens the database"""
    #book = piecash.open_book(filename, open_if_lock=True)
    book = create_book()
    return book

def create_book():
    """Creates a new in-memory book"""
    #piecash.create_book(filename)
    return piecash.create_book()
