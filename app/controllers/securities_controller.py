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
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securitiesaggregate import SecuritiesAggregate
from app.models import security_models


stock_controller = Blueprint( # pylint: disable=invalid-name
    'stock_controller', __name__, url_prefix='/security')


@stock_controller.route('/')
def stocks():
    """ Root """
    return render_template('incomplete.html')


@stock_controller.route('/analysis', methods=['GET'])
def security_analysis():
    """ Form for user input, entering the symbol """
    # load all non-currency symbols
    with BookAggregate() as svc:
        model = __get_model_for_analysis(svc)
        search = {
            "symbol": None,
            "action": "/security/analysis"
        }
        return render_template('security.analysis.html', model=model, filter=search)


@stock_controller.route('/analysis/<symbol>')
def security_analysis_symbol(symbol: str):
    """ displays the details in a separate page. Restful url. """
    with BookAggregate() as svc:
        sec = svc.securities.get_by_symbol(symbol)
        log(DEBUG, "stock returned: %s", sec)

        model = security_models.SecurityDetailsViewModel()
        model.security = sec

        # TODO load all accounts
        #model.accounts

        return render_template('security.details.html', model=model)


@stock_controller.route('/analysis', methods=['POST'])
def security_analysis_post():
    """ Displays the results """
    with BookAggregate() as svc:
        model = __get_model_for_analysis(svc.book)
        search = __parse_input_model()
        return render_template('security.analysis.html', model=model, filter=search)


def __get_model_for_analysis(svc: BookAggregate):
    """ Loads model for analysis """
    service = SecuritiesAggregate(svc.book)
    all_securities = service.get_all()
    # retrieve the view model
    security_list = {}
    for stock in all_securities:
        security_list[stock.mnemonic] = stock.fullname
    model = {
        "securities": security_list
    }
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
