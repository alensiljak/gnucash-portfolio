""" Price controller """
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib.bookaggregate import BookAggregate
from gnucash_portfolio.lib.database import Database

price_controller = Blueprint('price_controller', __name__, url_prefix='/price')

@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')

@price_controller.route('/import')
def import_prices():
    """ Stock price import """
    return render_template('incomplete.html')

class RateViewModel:
    """ View model for exchange rate """
    def __init__(self):
        self.date = None
        self.value = 0
        self.currency = ""
        self.base_currency = ""


@price_controller.route('/rates')
def import_rates():
    """ currency exchange rates """
    rates = []
    # get all used currencies and their (latest?) rates
    with Database().open_book() as book:
        svc = BookAggregate(book)
        currencies = svc.get_currencies()
        for cur in currencies:
            # Name
            rate = RateViewModel()
            rate.currency = cur.mnemonic
            # Rate
            cur_svc = svc.get_currency_aggregate(cur)
            price = cur_svc.get_latest_price()
            if price:
                rate.date = price.date
                rate.value = price.value
                #print(price.commodity.mnemonic)
                rate.base_currency = price.currency.mnemonic

            rates.append(rate)

        output = render_template('price.rates.html', rates=rates)
    return output
