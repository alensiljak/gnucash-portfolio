"""
Import currency exchange rates from .csv file into GnuCash
"""
import logging

from sqlalchemy import func

from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib import settings


class ExchangeRatesImporter:
    def __init__(self):
        self.settings = settings.Settings()

    def get_latest_rates(self):
        with BookAggregate() as svc:
            book_currencies = svc.currencies.get_book_currencies()
            base_currency = svc.currencies.get_default_currency()

        # Currencies to be downloaded/imported.
        currencies = [currency.mnemonic for currency in book_currencies]
        logging.debug(f"requested currencies: {currencies}")

        # Base currency. Required for downloading the currency pairs.
        logging.debug(f"Base currency: {base_currency}")

        # self.settings
        # TODO rateman = currencyrates.CurrencyRatesRetriever()
        # Get the rates json.
        #currencies = ["AUD", "USD"]
        # TODO refactor this to receive the list of currencies
        # TODO latest = rateman.download("CURRENCY", "AUD", "EUR")

        # iterate over rates and display rates for specified currencies only.
        # rates = latest["rates"]
        # log(DEBUG, "Rates for %s", latest["date"])
        # for currency in currencies:
        #     value = rates[currency]
        #     log(DEBUG, base_currency + '/' + currency, value)

        # TODO redo this to use finance::quote package
        latest = None
        return latest

    def display_gnucash_rates(self):
        with BookAggregate() as svc:
            # display prices for all currencies as the rates are expressed in the base currency.
            for currency in svc.book.currencies:
                prices = currency.prices.all()
                if prices:
                    logging.debug(currency.mnemonic)
                    for price in prices:
                        logging.debug(price)

    def get_count(self, query):
        """
        Returns a number of query results. This is faster than .count() on the query
        """
        count_q = query.statement.with_only_columns(
            [func.count()]).order_by(None)
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

    # translate into an array of PriceModels
    # TODO mapper = currencyrates.FixerioModelMapper()
    mapper = None
    rates = mapper.map_to_model(latest_rates_json)

    print("####################################")
    print("importing rates into gnucash...")
    # For writing, use True below.
    with BookAggregate(for_writing=False) as svc:
        svc.currencies.import_fx_rates(rates)

    print("####################################")
    print("displaying rates from gnucash...")
    importer.display_gnucash_rates()


###############################################################################
if __name__ == "__main__":
    main()
