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

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock')


@stock_controller.route('/')
def stocks():
    """ Root """
    return render_template('incomplete.html')


@stock_controller.route('/analysis')
def security_analysis():
    """ Form for user input, entering the symbol """
    # load all non-currency symbols
    with BookAggregate() as svc:
        book = svc.book
        service = SecuritiesAggregate(book)
        all_securities = service.get_all()
        # retrieve the view model
        security_list = {}
        for stock in all_securities:
            security_list[stock.mnemonic] = stock.fullname
        model = {
            "securities": security_list
        }

    # render output
    return render_template('security.analysis.html', model=model)


@stock_controller.route('/transactions/<symbol>')
def transactions():
    """ Lists all transactions for security. Symbol must include namespace. """

