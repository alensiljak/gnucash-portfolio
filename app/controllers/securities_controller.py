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


@stock_controller.route('/details/<symbol>')
def details(symbol: str):
    """ Displays the details in a separate page. Restful url. """
    with BookAggregate() as svc:
        sec = svc.securities.get_by_symbol(symbol)
        sec_agg = svc.securities.get_aggregate(sec)

        model = security_models.SecurityDetailsViewModel()
        model.security = sec
        # Quantity
        model.quantity = sec_agg.get_num_shares()

        # load all accounts
        sec_agg = svc.securities.get_aggregate(sec)
        model.accounts = sec_agg.accounts

        return render_template('security.details.html', model=model)


# @stock_controller.route('/analysis', methods=['POST'])
# def security_analysis_post():
#     """ Displays the results """
#     with BookAggregate() as svc:
#         model = __get_model_for_analysis(svc.book)
#         search = __parse_input_model()
#         return render_template('security.analysis.html', model=model, filter=search)


def __get_model_for_analysis(svc: BookAggregate):
    """ Loads model for analysis """
    service = SecuritiesAggregate(svc.book)
    all_securities = service.get_all()

    model = security_models.SecurityAnalysisRefModel()
    model.securities = all_securities

    return model


def __parse_input_model():
    """ Parses the filter from request """
    result = security_models.StockAnalysisInputModel()

    result.symbol = request.form.get("search.symbol")
    print(result.symbol)

    return result


@stock_controller.route('/transactions/<symbol>')
def transactions():
    """ Lists all transactions for security. Symbol must include namespace. """
    return render_template('incomplete.html')
