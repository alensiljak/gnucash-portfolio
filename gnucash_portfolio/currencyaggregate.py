""" Currencies service """
from sqlalchemy import desc
from piecash import Book, Commodity, Price

class CurrencyAggregate():
    """ Service/aggregate for currencies """
    def __init__(self, currency: Commodity):
        """ constructor """
        #self.book = book
        self.currency = currency

    def get_latest_price(self) -> Price:
        """ Returns the latest price entity """
        #stmt = select([test]).
        latest_price = self.currency.prices.order_by(desc(Price.date)).first()
        return latest_price

    def get_latest_rate_with(self, other: Commodity) -> Price:
        """ Fetches the latest available rate for the currency pair """
        result = (self.currency.prices
                  .filter(Price.commodity == self.currency, Price.currency == other)
                  .first()
        )
        print("latest rate", self.currency.mnemonic, other.mnemonic, result)
        return result
