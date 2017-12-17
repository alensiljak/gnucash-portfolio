"""
Portfolio
- cash account balances per currency
- portfolio value report
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import portfoliovalue, database

portfolio_controller = Blueprint('portfolio_controller', __name__, 
                                 url_prefix='/portfolio')


@portfolio_controller.route('/value')
def portfolio_value():
    """ Portfolio Value report """
    stock_rows = []
    with database.Database().open_book() as book:
        all_stocks = portfoliovalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in all_stocks:
            model = portfoliovalue.get_stock_model_from(book, stock)
            stock_rows.append(model)

    return render_template('portfolio.value.html', stock_rows=stock_rows)
