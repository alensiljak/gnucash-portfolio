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

currency_controller = Blueprint('currency_controller', __name__, url_prefix='/currency')


@currency_controller.route('/')
def index():
    """ This should be the query that other, more specific filters can use
    by passing parameters. """
    with Database().open_book() as book:
        search_model = SearchModel()
        search_model.init_from_book(book)

        output = render_template('currency.html', search_model=search_model)
    return output

@currency_controller.route('/search', methods=['GET', 'POST'])
def post():
    """ Receives post form """
    # init the search form model
    search_model = SearchModel()

    with Database().open_book() as book:
        search_model.initialize(book, request)

        model = __search(book, search_model)
        return render_template('currency.html', model=model, search_model=search_model)


class SearchModel:
    """ Model with static data for the search form. """
    def __init__(self):
        self.action = "/currency/search"
        self.currencies = []
        self.currency = None

    def initialize(self, book: Book, request):
        """ Initialize full search model """
        if book:
            self.init_from_book(book)

        if request:
            self.init_from_request(request)

    def init_from_book(self, book: Book):
        """ Populate the static model from the database """
        self.currencies = book.currencies

    def init_from_request(self, request):
        """ Initialize selected values """
        #print(request.path)
        #print(request.url_rule)
        self.currency = request.form.get("search.currency")


###############################################################################

def __search(book: Book, model: SearchModel):
    """ performs the search """
    query = (
        book.session.query(Commodity)
        .filter(Commodity.namespace == "CURRENCY")
    )

    if model.currency:
        query.filter(Commodity.mnemonic == model.currency)

    return query.all()
