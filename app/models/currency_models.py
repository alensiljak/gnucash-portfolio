""" Models for currency controller """
from piecash import Book, Commodity
from gnucash_portfolio.bookaggregate import BookAggregate
#from types import SimpleNamespace


class SearchReferenceModel:
    """ Model with reference data """
    def __init__(self):
        self.currencies = []

    def init_from_book(self, book: Book):
        """ Populate the static model from the database """
        #splits.sort(key=lambda split: split.transaction.post_date)
        svc = BookAggregate()
        svc.book = book
        self.currencies = (
            svc.get_currencies_query()
            .order_by(Commodity.mnemonic)
        )


class CurrencySearchModel:
    """ Model with static data for the search form. """
    def __init__(self):
        # these are the selected values
        self.action = "/currency/search"
        self.currency = None

        self.ref = SearchReferenceModel()

    def initialize(self, book: Book, request):
        """ Initialize full search model """
        if book:
            self.ref.init_from_book(book)

        if request:
            self.init_from_request(request)

        return self

    def init_from_request(self, request):
        """ Initialize selected values """
        #print(request.path)
        #print(request.url_rule)
        self.currency = request.form.get("search.currency")
