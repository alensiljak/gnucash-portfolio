""" Currencies service """
from sqlalchemy import desc
from piecash import Book, Commodity, Price

class CurrencyAggregate():
    """ Service/aggregate for currencies """
    def __init__(self, book: Book):
        """ constructor """
        self.book = book
        #self.currency = currency

    def get_latest_price(self, currency: Commodity) -> Price:
        """ Returns the latest price entity """
        #stmt = select([test]).
        latest_price = currency.prices.order_by(desc(Price.date)).first()
        return latest_price

    def get_latest_rate(self, currency: Commodity, other: Commodity) -> Price:
        """ Fetches the latest available rate for the currency pair """
        query = (
            currency.prices
            .filter(Price.commodity == currency, Price.currency == other)
            )
        #print("latest rate", currency.mnemonic, other.mnemonic, result)
        return query.first()

    def get_currency_by_symbol(self, symbol: str) -> Commodity:
        """ Loads currency by symbol """
        query = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace == "CURRENCY", Commodity.mnemonic == symbol)
        )
        return query.one()
