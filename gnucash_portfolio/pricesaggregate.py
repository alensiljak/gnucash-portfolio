""" Prices """

from logging import log, INFO, WARN
from typing import List
from datetime import datetime
from sqlalchemy import desc, or_
from piecash import Book, Commodity, Price
from gnucash_portfolio.model.price_model import PriceModel
from gnucash_portfolio.securitiesaggregate import SecurityAggregate


class PricesAggregate:
    """ handle price collections """
    def __init__(self, book: Book):
        self.book = book

    def get_price_as_of_query(self, stock: Commodity, on_date: datetime):
        """ Gets the price for commodity on given date or last known before the date """
        query = (
            self.book.session.query(Price)
            .filter(Price.date <= on_date,
                    Price.commodity == stock)
            .order_by(desc(Price.date))
        )
        return query

    def get_price_as_of(self, stock: Commodity, on_date: datetime):
        """ Gets the latest price on or before the given date. """
        return self.get_price_as_of_query(stock, on_date).first()

    def get_for_symbol(self, symbol: str) -> List[Price]:
        # get commodity
        cdty = self.__get_commodity(symbol)
        return cdty.prices

    def import_prices(self, prices: List[PriceModel]):
        """ Import prices (from csv) """
        result = {}
        for price in prices:
            result[price.name] = self.__import_price(price)

        return result

    #################
    # Private

    def __import_price(self, price: PriceModel):
        """ Import individual price """
        stock = self.__get_commodity(price.name)
        if stock is None:
            log(WARN, "security %s not found in book.", price.name)
            return False

        # check if there is already a price for the date
        existing_prices = stock.prices.filter(Price.date == price.date).all()
        if not existing_prices:
            # Create new price for the commodity (symbol).
            self.__create_price_for(stock, price)
        else:
            log(WARN, "price already exists for %s on %s",
                stock.mnemonic, price.date.strftime("%Y-%m-%d"))

            existing_price = existing_prices[0]
            # update price
            existing_price.value = price.value

        return True

    def __get_commodity(self, symbol: str):
        """ Loads the stock from the book. Symbol is yahoo-style symbol """
        # TODO: use the securities aggregate

        # Handle yahoo-style symbols with extension.
        symbol_only = symbol.split(".")[0]

        securities = (
            self.book.session.query(Commodity)
            .filter(
                Commodity.namespace != "template", 
                Commodity.namespace != "CURRENCY",
                or_(Commodity.mnemonic.ilike(symbol_only), 
                    Commodity.mnemonic.ilike(symbol))
            )
        ).all()

        security = None

        if not securities:
            log(WARN, "Could not find security %s", symbol_only)
            return None
        if len(securities) > 1:
            raise ValueError("More than one security found for", symbol)

        #if len(securities) == 1:
        security = securities[0]

        return security

    def __create_price_for(self, commodity: Commodity, price: PriceModel):
        """
        Creates a new Price entry in the book, for the given commodity.
        """
        log(INFO, "Adding a new price for %s, %s, %s",
            commodity.mnemonic, price.date.strftime("%Y-%m-%d"), price.value)

        #currency = commodity.book.currencies.get(mnemonic=commodity.mnemonic)
        sec_svc = SecurityAggregate(self.book, commodity)
        currency = sec_svc.get_currency()

        if currency.mnemonic != price.currency:
            raise ValueError(
                "Requested currency does not match the currency previously used",
                currency.mnemonic, price.currency)

        new_price = Price(commodity, currency, price.date, price.value, 
            source="user:gnucash-portfolio")
        commodity.prices.append(new_price)


class PriceAggregate:
    """ handle individual price """
    def __init__(self, book: Book, price: Price):
        self.price = price
        self.book = book
