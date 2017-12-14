"""
Securities service layer
"""
from piecash import Book, Commodity
from gnucash_portfolio.lib import database
from typing import List

class Securities:
    """ Provides various functionality related to securities """

    def __init__(self, book: Book):
        self.book = book

    def get_all(self):
        """ Loads all non-currency commodities, assuming they are stocks. """
        query = (
            self.__get_base_query()
            .order_by(Commodity.mnemonic)
        )
        return query.all()


    def get_by_symbol(self, symbol: str) -> List[Commodity]:
        """ Returns all commodities with the given symbol """
        query = (
            self.__get_base_query()
            .filter(Commodity.mnemonic == symbol)
        )
        return query.all()


    def __get_base_query(self):
        """ Returns the base query which filters out data for all queries. """
        query = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace != "CURRENCY",
                    Commodity.namespace != "template")
        )
        return query


    def test(self):
        """ test-only method """
        print("I'm alive!")

######################################################################
if __name__ == "__main__":
    Securities(None).test()
 