#!/usr/bin/python3
"""
Import currency exchange rates from .csv file into GnuCash
"""
from lib import database
from lib import settings
from piecash import Commodity
import csv
from os import path
from lib import currencyratesretriever

settings_path = "settings.json"

# def load_rates():
#     """Loads rates from .csv file"""
#     # todo: load rates from .csv
#     file_path = path.relpath('data/exchangeRates.csv')
#     with open(file_path, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader:
#             print(', '.join(row))
#     return ['rate1', 'rate2']

config = None

def get_settings():
    return settings.Settings(settings_path)

def main(book):
    config = get_settings()
    # Currencies to be downloaded/imported.
    currencies = config.get_currencies()
    print("requested currencies: ", currencies)

    print("Base currency:", config.base_currency)

    # Show the latest rate info?
    rateman = currencyratesretriever.CurrencyRatesRetriever(config)

    # download latest rates.
    print("Downloading rates...")
    latest = rateman.get_latest_rates()
    #print(latest)

    # iterate over rates and import for specified currencies only.
    rates = latest["rates"]
    print("Rates for", latest["date"])
    for currency in currencies:
        value = rates[currency]
        print(config.base_currency + '/' + currency, value)

    # todo import rates into gnucash file.

if __name__ == "__main__":
    with database.Database().open_book() as book:
        main(book)
        #db = database.Database()
        #db.display_db_info()
    