""" Currencies service """
from piecash import Book, Commodity

class CurrencyAggregate():
    """ Service/aggregate for currencies """
    def __init__(self, book: Book):
        """ constructor """
        self.book = book


    def get_book_currencies_query(self):
        """ Loads currencies used in the book """
        #book.currencies.sort(key=lambda currency: currency.mnemonic)
        query = (
            self.book.session.query(Commodity).filter_by(namespace="CURRENCY")
        )

        return query
