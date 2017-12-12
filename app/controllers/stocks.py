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

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock')

@stock_controller.route('/')
def stocks():
    return render_template('incomplete.html')

@stock_controller.route('/analysis')
def security_analysis():
    """ Form for user input, entering the symbol """
    # TODO load all non-currency symbols
    model = {}
    return render_template('stock.analysis.html', model=model)
