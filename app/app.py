"""
This is the entry point to the application
"""
import sys
#import logging
from flask import Flask, render_template, request
from gnucash_portfolio import get_vanguard_au_prices
from gnucash_portfolio.lib import assetallocation, settings, portfoliovalue, database

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')

@app.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')


@app.route('/vanguardprices')
def vanguard():
    """ Prices for Vanguard funds """
    #funds = "8123,8146,8148,8147"
    #print(request.form.get("funds"))
    funds = request.args.get("funds")
    prices = None

    if funds:
        print("funds:", funds)
        user_funds = funds.strip().split(",")
        prices = get_vanguard_au_prices.download_fund_prices(user_funds)

    return render_template('vanguard_prices.html', prices=prices, funds=funds)


@app.route('/assetallocation')
def asset_allocation():
    """ Asset Allocation """
    book_url = settings.Settings().database_uri
    model = assetallocation.load_asset_allocation_model(book_url)
    return render_template('assetallocation.html', model=model)


@app.route('/portfoliovalue')
def portfolio_value():
    """ Portfolio Value report """
    stock_rows = []
    with database.Database().open_book() as book:
        all_stocks = portfoliovalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in all_stocks:
            model = portfoliovalue.get_stock_model_from(book, stock)
            stock_rows.append(model)

    #print(stock_rows)
    return render_template('portfolio_value.html', stock_rows=stock_rows)

##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
