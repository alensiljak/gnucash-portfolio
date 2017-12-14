"""
Currencies
- list of book currencies
- price import
- price cleanup / deletion
- exchange rate chart
"""
from flask import Blueprint, request, render_template
from piecash import Book
from gnucash_portfolio.lib.database import Database

currency_controller = Blueprint('currency_controller', __name__, url_prefix='/currency')


@currency_controller.route('/')
def index():
    """ This should be the free query that other, more specific filters can point to """
    model = {}
    with Database().open_book() as book:
        model["search"] = __load_search_model(book)
        return render_template('currency.html', model=model)


def __load_search_model(book: Book):
    """ Loads the data for the search model """
    model = {}
    # TODO load list of used currencies
    model["currencies"] = book.currencies

    return model
