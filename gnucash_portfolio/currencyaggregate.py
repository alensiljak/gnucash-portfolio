""" Currencies service """

from typing import List
from sqlalchemy import desc
from piecash import Book, Commodity, Price


class CurrencyAggregate():
    """ Service/aggregate for a single currency """
    def __init__(self, book: Book, currency: Commodity):
        """ constructor """
        self.book = book
        self.currency = currency

    def get_latest_rate(self, other: Commodity) -> Price:
        """ Fetches the latest available rate for the currency pair """
        query = (
            self.currency.prices
            .filter(Price.commodity == self.currency,
                    Price.currency == other)
            )
        return query.first()

    def get_latest_price(self) -> Price:
        """ Returns the latest price entity """
        query = (
            self.currency.prices
            .order_by(desc(Price.date))
        )
        latest_price = query.first()
        return latest_price


class CurrenciesAggregate():
    """ Service/aggregate for currencies """
    def __init__(self, book: Book):
        """ constructor """
        self.book = book


    @property
    def currencies_query(self):
        """ returns the query only """
        return (
            self.book.session.query(Commodity)
            .filter_by(namespace="CURRENCY")
        )


    @property
    def currencies_query_sorted(self):
        """ currencies, sorted alphabetically """
        return self.currencies_query.order_by(Commodity.mnemonic)


    def get_book_currencies(self) -> List[Commodity]:
        """ Returns currencies used in the book """
        query = (
            self.currencies_query
            .order_by(Commodity.mnemonic)
        )
        return query.all()


    def get_currency_aggregate(self, cur: Commodity) -> CurrencyAggregate:
        """ Returns a single-currency aggregate """
        return CurrencyAggregate(self.book, cur)


    def get_currency_by_symbol(self, symbol: str) -> Commodity:
        """ Loads currency by symbol """
        query = (
            self.currencies_query
            .filter(Commodity.mnemonic == symbol)
        )
        return query.one()
