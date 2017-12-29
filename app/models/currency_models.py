""" Models for currency controller """

from decimal import Decimal
from piecash import Book
from gnucash_portfolio.bookaggregate import BookAggregate


class SearchReferenceModel:
    """ Model with reference data """
    def __init__(self):
        self.currencies = []

    def init_from_book(self, book: Book):
        """ Populate the static model from the database """
        #splits.sort(key=lambda split: split.transaction.post_date)
        svc = BookAggregate()
        svc.book = book
        self.currencies = svc.currencies.get_book_currencies()


class CurrencySearchModel:
    """ Model with static data for the search form. """
    def __init__(self):
        # these are the selected values
        self.action: str = "/currency/search"
        self.currency: str = None

        self.ref: SearchReferenceModel = SearchReferenceModel()

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

#@dataclass
class RateViewModel:
    """ View model for exchange rate """
    def __init__(self):
        self.date = None
        self.value: Decimal = 0
        self.currency = ""
        self.base_currency = ""
