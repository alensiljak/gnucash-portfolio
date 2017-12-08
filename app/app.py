"""
This is the entry point to the application
"""
import sys
#import logging
from flask import Flask, render_template, request
from gnucash_portfolio import get_vanguard_au_prices
from gnucash_portfolio.lib import assetallocation, settings

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')

@app.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')


@app.route('/vanguard_prices')
def vanguard():
    """ Prices for Vanguard funds """
    return render_template('vanguard_prices.html')


@app.route('/vanguard_prices', methods=['POST'])
def vanguard_display():
    """ Example of accepting user input """
    fund_ids = "8123,8146,8148,8147"
    user_funds = fund_ids.strip().split(",")
    prices = get_vanguard_au_prices.download_fund_prices(user_funds)

    #logger = logging.getLogger(__name__)
    #logger.

    print(prices)
    #print(prices, file=sys.stderr)
    return render_template('vanguard_prices.html')


@app.route('/assetallocation')
def asset_allocation():
    """ Asset Allocation """
    book_url = settings.Settings().database_uri
    model = assetallocation.load_asset_allocation_model(book_url)
    return render_template('assetallocation.html', model=model)


@app.route('/portfoliovalue')
def portfolio_value():
    """ Portfolio Value report """
    return render_template('portfolio_value.html')

##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
