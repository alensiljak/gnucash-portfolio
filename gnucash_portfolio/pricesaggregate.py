""" Prices """

import csv
from datetime import datetime
from sqlalchemy import desc
from piecash import Book, Commodity, Price
from gnucash_portfolio.lib import database, price as pricelib


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

    def get_prices_from_csv(self, content: str):
        """ Imports prices from CSV content. See data folder for a sample file/content. """
        prices = []
        
        print("Trying to read prices from", content)
        reader = csv.reader(content)
        for row in reader:
            price = pricelib.Price()
            price.date = price.parse_euro_date(row[2])
            price.name = row[0]
            price.value = price.parse_value(row[1])
            #price.currency = "EUR"

            prices.append(price)
        return prices

class PriceAggregate:
    """ handle individual price """
    def __init__(self, book: Book, price: Price):
        self.price = price
