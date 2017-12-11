"""
This is the entry point to the application
"""
import sys
#from decorators import templated
#import logging
from flask import Flask, render_template, request
from gnucash_portfolio import get_vanguard_au_prices
from gnucash_portfolio.lib import assetallocation as aalloc, settings, portfoliovalue as pvalue, database
# Controllers/blueprints
from controllers.vanguardcontroller import vanguard_controller
from controllers.incomecontroller import income_controller

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')
# Register blueprints
app.register_blueprint(vanguard_controller)
app.register_blueprint(income_controller)

@app.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')


@app.route('/assetallocation')
#@templated()
def assetallocation():
    """ Asset Allocation """
    book_url = settings.Settings().database_uri
    model = aalloc.load_asset_allocation_model(book_url)
    return render_template('assetallocation.html', model=model)
    #return dict(model=model)


@app.route('/portfoliovalue')
#@templated()
def portfoliovalue():
    """ Portfolio Value report """
    stock_rows = []
    with database.Database().open_book() as book:
        all_stocks = pvalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in all_stocks:
            model = pvalue.get_stock_model_from(book, stock)
            stock_rows.append(model)

    #print(stock_rows)
    return render_template('portfolio_value.html', stock_rows=stock_rows)
    #return dict(stock_rows=stock_rows)


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
