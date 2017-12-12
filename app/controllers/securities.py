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
from gnucash_portfolio.lib import securities
from gnucash_portfolio.lib.database import Database

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock')


@stock_controller.route('/')
def stocks():
    return render_template('incomplete.html')


@stock_controller.route('/analysis')
def security_analysis():
    """ Form for user input, entering the symbol """
    # load all non-currency symbols
    with Database().open_book() as book:
        service = securities.Securities(book)
        all_securities = service.load_all_stocks()
        # retrieve the view model
        security_list = {}
        for stock in all_securities:
            security_list[stock.mnemonic] = stock.fullname
        model = {
            "securities": security_list
        }

    # render output
    return render_template('stock.analysis.html', model=model)
