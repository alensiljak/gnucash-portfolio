"""
Import currency exchange rates from .csv file into GnuCash
"""
#from pprint import pprint
from lib import database
from lib import settings
from piecash import Commodity
import csv
from os import path

settings_path = "settings.json"

def load_rates():
    """Loads rates from .csv file"""
    # todo: load rates from .csv
    file_path = path.relpath('data/exchangeRates.csv')
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
    return ['rate1', 'rate2']

def get_settings():
    return settings.Settings(settings_path)

def main(book):
    config = get_settings()
    currencies = config.get_currencies()
    print("requested currencies: ", currencies)

    # todo: load the rates from the file
    rates = load_rates()
    # todo: iterate over rates and import for specified currencies only.
    for rate in rates:
        print(rate)

#with Database().open_book() as book:
    # do something
    #main(book)
if __name__ == "__main__":
    db = database.Database()
    db.display_db_info()
    