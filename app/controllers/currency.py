"""
Currencies
- list of book currencies
- price import
- price cleanup / deletion
- exchange rate chart
"""
from flask import Blueprint, request, render_template
from piecash import Commodity
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.bookaggregate import BookAggregate
from app.models.currency_models import CurrencySearchModel


currency_controller = Blueprint( # pylint: disable=invalid-name
    'currency_controller', __name__, url_prefix='/currency')


@currency_controller.route('/')
def index():
    """ This should be the query that other, more specific filters can use
    by passing parameters. """
    with Database().open_book() as book:
        search_model = CurrencySearchModel().initialize(book, None)
        output = render_template('currency.html', search=search_model)
    return output


@currency_controller.route('/search', methods=['GET', 'POST'])
def post():
    """ Receives post form """
    with BookAggregate as svc:
        search_model = CurrencySearchModel().initialize(svc.book, request)
        currency = __search(svc, search_model)
        output = render_template('currency.html', currency=currency, search=search_model)
    return output


###############################################################################

def __search(svc: BookAggregate, model: CurrencySearchModel):
    """ performs the search """
    query = svc.get_currencies_query()

    if model.currency:
        query = query.filter(Commodity.mnemonic == model.currency)

        # TODO if not the main currency, load exchange rates and display chart
        if model.ref.currencies != svc.get_default_currency():
            print("not the default currency. load data.")

    return query.one()
