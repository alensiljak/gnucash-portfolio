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

__config = None

def get_settings():
    global __config
    if __config is None:
        __config = settings.Settings(settings_path)
    return __config

def __get_latest_rates():
    config = get_settings()
    # Currencies to be downloaded/imported.
    currencies = config.get_currencies()
    print("requested currencies: ", currencies)

    # Base currency. Required for downloading the currency pairs.
    print("Base currency:", config.base_currency)

    rateman = currencyratesretriever.CurrencyRatesRetriever(config)
    latest = rateman.get_latest_rates()

    # iterate over rates and import for specified currencies only.
    rates = latest["rates"]
    print("Rates for", latest["date"])
    for currency in currencies:
        value = rates[currency]
        print(config.base_currency + '/' + currency, value)

    return rates

def main():
    config = get_settings()

    rates = __get_latest_rates()

    # todo import rates into gnucash

    # todo display rates from gnucash
    with database.Database().open_book() as book:
        book.get(Commodity, mnemonic=config.base_currency)


if __name__ == "__main__":
    main()
    