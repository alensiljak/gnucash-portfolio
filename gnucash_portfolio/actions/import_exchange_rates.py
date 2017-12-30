#!/usr/bin/python3
"""
Import currency exchange rates from .csv file into GnuCash
"""
from typing import List
from logging import log, INFO, DEBUG
#from datetime import datetime
from sqlalchemy import func
from piecash import Price
from gnucash_portfolio.lib import currencyrates, settings
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.model.price_model import PriceModel


class ExchangeRatesImporter:
    def __init__(self):
        self.settings = settings.Settings()

    def get_latest_rates(self):
        with BookAggregate() as svc:
            book_currencies = svc.currencies.get_book_currencies()
            base_currency = svc.currencies.get_default_currency()

        # Currencies to be downloaded/imported.
        currencies = [currency.mnemonic for currency in book_currencies]
        log(DEBUG, "requested currencies: ", currencies)

        # Base currency. Required for downloading the currency pairs.
        log(DEBUG, "Base currency:", base_currency)

        rateman = currencyrates.CurrencyRatesRetriever(self.settings)
        # Get the rates json.
        latest = rateman.get_latest_rates()

        # iterate over rates and display rates for specified currencies only.
        rates = latest["rates"]
        log(DEBUG, "Rates for %s", latest["date"])
        for currency in currencies:
            value = rates[currency]
            log(DEBUG, base_currency + '/' + currency, value)

        return latest

    def display_gnucash_rates(self):
        with BookAggregate() as svc:
            # display prices for all currencies as the rates are expressed in the base currency.
            for currency in svc.book.currencies:
                prices = currency.prices.all()
                if prices:
                    log(DEBUG, currency.mnemonic)
                    for price in prices:
                        log(DEBUG, price)

    def get_count(self, query):
        """
        Returns a number of query results. This is faster than .count() on the query
        """
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        count = query.session.execute(count_q).scalar()
        return count

#####################################

def main():
    """
    Default entry point
    """
    importer = ExchangeRatesImporter()

    print("####################################")
    latest_rates_json = importer.get_latest_rates()

    # TODO translate into an array of PriceModels
    mapper = currencyrates.FixerioModelMapper()
    rates = mapper.map_to_model(latest_rates_json)

    print("####################################")
    print("importing rates into gnucash...")
    importer.save_rates(rates)

    print("####################################")
    print("displaying rates from gnucash...")
    importer.display_gnucash_rates()

###############################################################################
if __name__ == "__main__":
    main()
    