""" Prices """

import logging
from typing import List
from datetime import datetime
from piecash import Book, Commodity, Price
from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate
from pricedb import PriceDbApplication, PriceModel, SecuritySymbol


class PricesAggregate:
    """ Handle price collections. Uses PriceDb library. """

    def __init__(self, book: Book):
        self.book = book

    # def get_price_as_of_query(self, stock: Commodity, on_date: datetime):
    #     """ Gets the price for commodity on given date or last known before the date """
    # query = (
    #     self.book.session.query(Price)
    #     .filter(Price.date <= on_date.date())
    #     .filter(Price.commodity == stock)
    #     .order_by(desc(Price.date))
    # )
    # return query

    def get_latest_price(self, security: Commodity) -> PriceModel:
        """ Returns the latest available price for commodity """
        assert isinstance(security, Commodity)

        symbol = SecuritySymbol(security.namespace, security.mnemonic)
        prices = PriceDbApplication()
        result = prices.get_latest_price(symbol)
        return result

    def get_price_as_of(self, stock: Commodity, on_date: datetime):
        """ Gets the latest price on or before the given date. """
        # return self.get_price_as_of_query(stock, on_date).first()
        prices = PriceDbApplication()
        prices.get_prices_on(on_date.date().isoformat(), stock.namespace, stock.mnemonic)

    # def get_for_symbol(self, symbol: str) -> List[Price]:
    #     # get commodity
    #     stock = SecuritiesAggregate(self.book).get_by_symbol(symbol)
    #     return stock.prices

    def import_prices(self, prices: List[PriceModel]):
        """ Import prices (from csv) """
        result = {}
        for price in prices:
            result[price.symbol] = self.import_price(price)

        return result

    def import_price(self, price: PriceModel):
        """ Import individual price """
        # Handle yahoo-style symbols with extension.
        symbol = price.symbol
        if "." in symbol:
            symbol = price.symbol.split(".")[0]
        stock = SecuritiesAggregate(self.book).get_by_symbol(symbol)
        # get_aggregate_for_symbol

        if stock is None:
            logging.warning("security %s not found in book.", price.symbol)
            return False

        # check if there is already a price for the date
        existing_prices = stock.prices.filter(Price.date == price.datetime.date()).all()
        if not existing_prices:
            # Create new price for the commodity (symbol).
            self.__create_price_for(stock, price)
        else:
            logging.warning("price already exists for %s on %s",
                            stock.mnemonic, price.datetime.strftime("%Y-%m-%d"))

            existing_price = existing_prices[0]
            # update price
            existing_price.value = price.value

        return True

    #################
    # Private

    def __create_price_for(self, commodity: Commodity, price: PriceModel):
        """ Creates a new Price entry in the book, for the given commodity """
        logging.info("Adding a new price for %s, %s, %s",
                     commodity.mnemonic, price.datetime.strftime("%Y-%m-%d"), price.value)

        # safety check. Compare currencies.
        sec_svc = SecurityAggregate(self.book, commodity)
        currency = sec_svc.get_currency()

        if currency != price.currency:
            raise ValueError(
                "Requested currency does not match the currency previously used",
                currency, price.currency)

        # Description of the source field values:
        # https://www.gnucash.org/docs/v2.6/C/gnucash-help/tool-price.html

        new_price = Price(commodity, currency, price.datetime.date(), price.value,
                          source="Finance::Quote")
        commodity.prices.append(new_price)


class PriceAggregate:
    """ handle individual price """

    def __init__(self, price: PriceModel):
        self.price = price
