"""
Currencies
- list of book currencies
- price import
- price cleanup / deletion
- exchange rate chart
"""
from flask import Blueprint, request, render_template
from piecash import Book, Commodity
from gnucash_portfolio.lib.database import Database
#from gnucash_portfolio.currencyaggregate import CurrencyAggregate
from gnucash_portfolio.bookaggregate import BookAggregate

currency_controller = Blueprint('currency_controller', __name__, url_prefix='/currency')


@currency_controller.route('/')
def index():
    """ This should be the query that other, more specific filters can use
    by passing parameters. """
    with Database().open_book() as book:
        search_model = SearchModel().initialize(book, None)
        output = render_template('currency.html', search=search_model)
    return output

@currency_controller.route('/search', methods=['GET', 'POST'])
def post():
    """ Receives post form """
    with BookAggregate as svc:
        search_model = SearchModel().initialize(svc.book, request)
        currency = __search(svc, search_model)
        output = render_template('currency.html', currency=currency, search=search_model)
    return output


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


class SearchModel:
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


###############################################################################

def __search(svc: BookAggregate, model: SearchModel):
    """ performs the search """
    query = svc.get_currencies_query()

    if model.currency:
        query = query.filter(Commodity.mnemonic == model.currency)

        # TODO if not the main currency, load exchange rates and display chart
        if model.ref.currencies != svc.get_default_currency():
            print("not the default currency. load data.")


    return query.one()
