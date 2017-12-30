"""
Currencies
- list of book currencies
- price import
- price cleanup / deletion
- exchange rate chart
"""
from logging import log, DEBUG
from flask import Blueprint, request, render_template
try: import simplejson as json
except ImportError: import json
from piecash import Commodity
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.lib import datetimeutils
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate
from gnucash_portfolio.model.price_model import PriceModel
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
    fx_rates = []
    # get all used currencies and their (latest?) rates
    with BookAggregate() as svc:
        base_currency = svc.currencies.get_default_currency()
        #print(base_currency)
        currencies = svc.currencies.get_book_currencies()
        for cur in currencies:
            # skip the base currency
            if cur == base_currency:
                continue

            # Name
            rate = RateViewModel()
            rate.currency = cur.mnemonic
            # Rate
            cur_svc = CurrencyAggregate(svc.book, cur)
            price = cur_svc.get_latest_price()
            if price:
                rate.date = price.date
                rate.value = price.value
                rate.base_currency = price.currency.mnemonic

            fx_rates.append(rate)

        output = render_template('price.rates.html', rates=fx_rates)
    return output

@currency_controller.route('/download')
def download():
    """ Download of exchange rates. React client-side app. """
    # get book currencies
    with BookAggregate() as svc:
        currencies = [cur.mnemonic for cur in svc.currencies.get_book_currencies()]
        model = {
            "currencies": currencies
        }
        return render_template('currency.download.html', model=model)

###############
# API

@currency_controller.route('/api/saverates', methods=['POST'])
def api_save_rates():
    """ Saves exchange rates """
    # parse data
    cur_json = request.form.get('currencies')
    base_cur_symbol = request.form.get('base')
    rate_date = datetimeutils.parse_iso_date(request.form.get("date"))
    fx_rates = json.loads(cur_json)
    # filter out the ones without rates
    filtered_rates = [item for item in fx_rates if "rate" in item]

    with BookAggregate() as svc:
        book_base_cur = svc.currencies.get_default_currency().mnemonic
        if book_base_cur != base_cur_symbol:
            raise ValueError("The base currencies are not same!", base_cur_symbol, "vs",
                             book_base_cur)
        # Import rates
        prices_model = ([PriceModel(symbol=in_rate["symbol"], base_cur=base_cur_symbol,
                                    value=in_rate["rate"], rate_date=rate_date)
                         for in_rate in filtered_rates])
        svc.currencies.import_fx_rates(prices_model)

    return "I'll think about it"

###############################################################################

def __search(svc: BookAggregate, model: CurrencySearchModel):
    """ performs the search """
    if not model.currency:
        return None

    query = svc.currencies.currencies_query_sorted

    if model.currency:
        query = query.filter(Commodity.mnemonic == model.currency)

        # TODO if not the main currency, load exchange rates and display chart
        if model.ref.currencies != svc.currencies.get_default_currency():
            print("not the default currency. load data.")

    return query.one()
