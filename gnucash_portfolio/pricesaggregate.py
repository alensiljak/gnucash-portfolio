""" Prices """

from datetime import datetime
from sqlalchemy import desc
from piecash import Book, Commodity, Price


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
        """ blah """
        return self.get_price_as_of_query(stock, on_date).first()

class PriceAggregate:
    """ handle individual price """
    def __init__(self, book: Book, price: Price):
        self.price = price
