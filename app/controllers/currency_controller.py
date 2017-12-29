"""
Currencies
- list of book currencies
- price import
- price cleanup / deletion
- exchange rate chart
"""
#from logging import debug
from flask import Blueprint, request, render_template
from piecash import Commodity
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate
from app.models.currency_models import CurrencySearchModel, RateViewModel


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
    with BookAggregate() as svc:
        search_model = CurrencySearchModel().initialize(svc.book, request)
        currency = __search(svc, search_model)
        output = render_template('currency.html', currency=currency, search=search_model)
    return output

@currency_controller.route('/rates')
def rates():
    """ currency exchange rates """
    rates = []
    # get all used currencies and their (latest?) rates
    with BookAggregate() as book_svc:
        base_currency = book_svc.get_default_currency()
        #print(base_currency)
        currencies = book_svc.currencies.get_book_currencies()
        for cur in currencies:
            # skip the base currency
            if cur == base_currency:
                continue

            # Name
            rate = RateViewModel()
            rate.currency = cur.mnemonic
            # Rate
            cur_svc = CurrencyAggregate(book_svc.book, cur)
            price = cur_svc.get_latest_price()
            if price:
                rate.date = price.date
                rate.value = price.value
                #print(price.commodity.mnemonic)
                rate.base_currency = price.currency.mnemonic

            rates.append(rate)

        output = render_template('price.rates.html', rates=rates)
    return output

@currency_controller.route('/download')
def download():
    """ Download exchange rates """
    return render_template('currency.download.html')


###############################################################################

def __search(svc: BookAggregate, model: CurrencySearchModel):
    """ performs the search """
    if not model.currency:
        return None

    query = svc.currencies.currencies_query_sorted

    if model.currency:
        query = query.filter(Commodity.mnemonic == model.currency)

        # TODO if not the main currency, load exchange rates and display chart
        if model.ref.currencies != svc.get_default_currency():
            print("not the default currency. load data.")

    return query.one()
