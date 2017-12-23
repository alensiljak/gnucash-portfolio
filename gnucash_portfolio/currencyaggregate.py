""" Currencies service """
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

    def get_currency_aggregate(self, cur: Commodity) -> CurrencyAggregate:
        """ Returns a single-currency aggregate """
        return CurrencyAggregate(self.book, cur)

    def get_currency_by_symbol(self, symbol: str) -> Commodity:
        """ Loads currency by symbol """
        query = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace == "CURRENCY", Commodity.mnemonic == symbol)
        )
        return query.one()
