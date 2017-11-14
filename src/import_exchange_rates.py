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
        #base_currency = book.get(Commodity, mnemonic=config.base_currency)

        # display prices for all currencies as the rates are expressed in the base currency.
        for currency in book.currencies:
            prices = currency.prices.all()
            if prices:
                print(currency.mnemonic)
                for price in prices:
                    print(price)

def __save_rates(config, latest_rates):
    '''
    Saves the rates to GnuCash
    '''
    base_symbol = config.base_currency

    with database.Database().open_book(for_writing=True) as book:
        base_currency = book.currencies.get(mnemonic=base_symbol)

        rate_date_string = latest_rates["date"]
        rate_date = datetime.strptime(rate_date_string, "%Y-%m-%d")
        # quotes = quandl_fx(self.mnemonic, default_currency.mnemonic, start_date)
        rates = latest_rates["rates"]
        have_new_rates = False

        for rate in rates:
            #print(rate, rates[rate])
            currency = book.currencies.get(mnemonic=rate)
            amount = rates[rate]

            # Do not import duplicate prices.
            # todo: if the price differs, update it!
            exists = currency.prices.filter(Price.date == rate_date).all()
            if not exists:
                print("Creating entry for", base_currency.mnemonic, currency.mnemonic, rate_date_string, amount)
                # Save the price in the exchange currency, not the default.
                # Invert the rate in that case.
                inverted_rate = 1 / amount;
                p = Price(commodity=currency,
                            currency=base_currency,
                            date=rate_date,
                            value=str(inverted_rate))
                have_new_rates = True
        
        # Save the book after the prices have been created.
        if have_new_rates:
            book.flush()
            book.save()
        else:
            print("No prices imported.")
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
    