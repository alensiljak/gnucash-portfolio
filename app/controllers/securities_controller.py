"""
Stocks
- List of all stocks (non-currency commodities)
- price chart for selectable period
- price import from csv
- list of all transactions (buy/sell)
- list of all distributions
- calculation of ROI
"""
from logging import log, DEBUG
import flask
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securitiesaggregate import SecuritiesAggregate
from app.models import security_models


stock_controller = Blueprint( # pylint: disable=invalid-name
    'stock_controller', __name__, url_prefix='/security')

@stock_controller.route('/')
def index():
    """ Root. Search form. """
    # Check if we have a symbol
    symbol = request.args.get('search.symbol')
    log(DEBUG, "symbol = %s, args: %s", symbol, request.args)
    if symbol:
        return flask.redirect(flask.url_for('stock_controller.details', symbol=symbol), code=307)
        # code 307, 302

    # else show the search form.
    with BookAggregate() as svc:
        model = __get_model_for_analysis(svc)
        search = {
            "symbol": None
        }
        return render_template('security.search.html', model=model, filter=search)

@stock_controller.route('/<symbol>/details')
def details(symbol: str):
    """ Displays the details in a separate page. Restful url. """
    with BookAggregate() as svc:
        model = __get_model_for_details(svc, symbol)
        return render_template('security.details.html', model=model)

@stock_controller.route('/details/partial/<symbol>')
def details_partial(symbol: str):
    """ Displays the details in a separate page. Restful url. """
    with BookAggregate() as svc:
        model = __get_model_for_details(svc, symbol)
        return render_template('_security.details.html', model=model)

def __get_model_for_details(
        svc: BookAggregate, symbol: str) -> security_models.SecurityDetailsViewModel:
    """ Loads the model for security details """
    sec = svc.securities.get_aggregate_for_symbol(symbol)

    model = security_models.SecurityDetailsViewModel()
    model.security = sec.security
    # Quantity
    model.quantity = sec.get_quantity()
    model.value = sec.get_value()
    model.currency = sec.get_currency().mnemonic
    model.price = sec.get_last_available_price()

    # load all accounts
    sec_agg = svc.securities.get_aggregate(sec)
    model.accounts = sec_agg.accounts

    return model

def __get_model_for_analysis(svc: BookAggregate):
    """ Loads model for analysis """
    service = SecuritiesAggregate(svc.book)
    all_securities = service.get_all()

    model = security_models.SecurityAnalysisRefModel()
    model.securities = all_securities

    return model

@stock_controller.route('/transactions/<symbol>')
def transactions():
    """ Lists all transactions for security. Symbol must include namespace. """
    return render_template('incomplete.html')

@stock_controller.route('/distributions/<symbol>')
def distributions():
    """ Distributions for the security """
    return render_template('distributions.html', model=None)
