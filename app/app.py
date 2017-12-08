"""
This is the entry point to the application
"""
from flask import Flask, render_template, request
from gnucash_portfolio import get_vanguard_au_prices

app = Flask(__name__)

@app.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')


@app.route('/vanguard_prices')
def vanguard():
    """ Prices for Vanguard funds """
    fund_ids = "8123,8146,8148,8147"
    user_funds = fund_ids.strip().split(",")
    prices = get_vanguard_au_prices.download_fund_prices(user_funds)
    return render_template('vanguard_prices.html')


@app.route('/vanguard_prices', methods=['POST'])
def vanguard_display():
    """ Example of accepting user input """
    return "Here we process the input from the user."


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    app.run(debug=True)
