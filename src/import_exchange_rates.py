#!/usr/bin/python3
"""
Import currency exchange rates from .csv file into GnuCash
"""
import csv
from sqlalchemy import func
from datetime import datetime, timedelta
import dateutil.parser
from piecash import Commodity, Price
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

    return latest

def __display_gnucash_rates(config):
    with database.Database().open_book() as book:
        base_currency = book.get(Commodity, mnemonic=config.base_currency)
        print("For base currency:", base_currency)

        prices = base_currency.prices
        #filter = prices.filter(Price.currency == base_currency)
        #today = dateutil.parser.parse(generic.get_today())
        yesterday = generic.get_yesterday()
        filter = prices.filter(Price.date == yesterday)
        print("there are following prices (", filter.count(), ")")

        for price in prices:
            print(price)

def __save_rates(config, latest_rates):
    '''
    Saves the rates to GnuCash
    '''
    base_symbol = config.base_currency

    with database.Database().open_book() as book:
        base_currency = book.currencies.get(mnemonic=base_symbol)

        #session = book.session
        #currencies = session.query(Commodity).filter(Commodity.namespace == "CURRENCY").all()
        #currencies_query = session.query(Commodity).filter(Commodity.namespace == "CURRENCY")
        #print("Commodities:", get_count(currencies_query))

        rate_date = latest_rates["date"]
        # quotes = quandl_fx(self.mnemonic, default_currency.mnemonic, start_date)
        rates = latest_rates["rates"]
        for rate in rates:
            #print(rate, rates[rate])
            currency = book.currencies.get(mnemonic=rate)
            amount = rates[rate]

            print("Creating entry for", base_currency, currency, rate_date, amount)
            p = Price(commodity=base_currency,
                        currency=currency,
                        date=datetime.strptime(rate_date, "%Y-%m-%d"),
                        value=str(amount))
            
            #base_currency.prices.add(p)
            #book.add(p)
            book.flush()
    return

def get_count(q):
    """
    Returns a number of query results. This is faster than .count() on the query
    """
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def main():
    """
    Default entry point
    """
    config = get_settings()

    print("####################################")
    latest_rates = __get_latest_rates(config)

    print("####################################")
    # todo import rates into gnucash
    __save_rates(config, latest_rates)

    print("####################################")
    # display rates from gnucash
    __display_gnucash_rates(config)

###############################################################################
if __name__ == "__main__":
    main()
    