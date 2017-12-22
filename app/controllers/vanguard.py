"""
Vanguard controller
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.actions import get_vanguard_au_prices

vanguard_controller = Blueprint( # pylint: disable=invalid-name
    'vanguard_controller', __name__, url_prefix='/vanguard')


@vanguard_controller.route('/')
def index():
    """ Root """
    return render_template("incomplete.html")


@vanguard_controller.route('/prices')
def vanguardprices():
    """ Prices for Vanguard funds """
    #funds = "8123,8146,8148,8147"
    #print(request.form.get("funds"))
    funds = request.args.get("funds")
    prices = None

    if funds:
        #print("funds:", funds)
        user_funds = funds.strip().split(",")
        prices = get_vanguard_au_prices.download_fund_prices(user_funds)

    return render_template('vanguard_prices.html', prices=prices, funds=funds)
    #return dict(prices=prices, funds=funds)
