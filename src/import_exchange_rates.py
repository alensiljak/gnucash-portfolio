#!/usr/bin/python3
"""
Import currency exchange rates from .csv file into GnuCash
"""
from datetime import datetime, timedelta
import dateutil.parser
from piecash import Commodity, Price
import csv
from os import path
from lib import currencyratesretriever
from lib import database
from lib import generic
from lib import settings


settings_path = "settings.json"

__config = None

def get_settings():
    """
    Returns the shared settings instance.
    """
    global __config
    if __config is None:
        __config = settings.Settings(settings_path)
    return __config

def __get_latest_rates(config):
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

def __display_gnucash_rates(config):
    with database.Database().open_book() as book:
        base_currency = book.get(Commodity, mnemonic=config.base_currency)
        print("Base currency:", base_currency)

        prices = base_currency.prices
        #filter = prices.filter(Price.currency == base_currency)
        #today = dateutil.parser.parse(generic.get_today())
        yesterday = datetime.today() - timedelta(days=1)
        filter = prices.filter(Price.date == yesterday)
        print(filter.count())
        
        for price in prices:
            print(price)

def __save_rates():
    # through Quandl for exchange rates
    # quotes = quandl_fx(self.mnemonic, default_currency.mnemonic, start_date)
    # for q in quotes:
    #     p = Price(commodity=self,
    #                 currency=default_currency,
    #                 date=datetime.datetime.strptime(q.date, "%Y-%m-%d"),
    #                 value=str(q.rate))
    return

def main():
    """
    Default entry point
    """
    config = get_settings()

    rates = __get_latest_rates(config)

    # todo import rates into gnucash
    #__import_rates(rates)

    # todo display rates from gnucash
    __display_gnucash_rates(config)

if __name__ == "__main__":
    main()
    