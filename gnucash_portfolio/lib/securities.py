"""
Securities service layer
"""
from piecash import Book, Commodity
from gnucash_portfolio.lib import database

class Securities:
    """ Provides various functionality related to securities """

    def __init__(self, book: Book):
        self.book = book

    def load_all_stocks(self):
        """ Loads all non-currency commodities, assuming they are stocks """
        all_securities = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace != "CURRENCY", Commodity.namespace != "template")
            .order_by(Commodity.mnemonic)
            .all()
        )
        return all_securities


    def test(self):
        """ test-only method """
        print("I'm alive!")

######################################################################
if __name__ == "__main__":
    Securities(None).test()
 