"""
Stocks
- List of all stocks (non-currency commodities)
- price chart for selectable period
- price import from csv
- list of all transactions (buy/sell)
- list of all distributions
- calculation of ROI
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securityaggregate import SecuritiesAggregate
from app.models.securities import StockAnalysisInputModel


stock_controller = Blueprint('stock_controller', __name__, url_prefix='/security')


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

@stock_controller.route('/analysis', methods=['POST'])
def security_analysis_post():
    """ Displays the results """
    with BookAggregate() as svc:
        model = __get_model_for_analysis(svc.book)
        search = __parse_input_model(request)
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

def __parse_input_model(request):
    """ Parses the filter from request """
    result = StockAnalysisInputModel()

    result.symbol = request.form.get("search.symbol")
    print(result.symbol)

    return result


@stock_controller.route('/transactions/<symbol>')
def transactions():
    """ Lists all transactions for security. Symbol must include namespace. """
    return render_template('incomplete.html')
