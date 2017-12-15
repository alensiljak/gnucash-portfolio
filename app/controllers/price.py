""" Price controller """
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate

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
    with BookAggregate() as book_svc:
        base_currency = book_svc.get_default_currency()
        #print(base_currency)
        currencies = book_svc.get_currencies()
        for cur in currencies:
            # skip the base currency
            if cur == base_currency:
                continue

            # Name
            rate = RateViewModel()
            rate.currency = cur.mnemonic
            # Rate
            cur_svc = CurrencyAggregate(book_svc.book)
            price = cur_svc.get_latest_price(cur)
            if price:
                rate.date = price.date
                rate.value = price.value
                #print(price.commodity.mnemonic)
                rate.base_currency = price.currency.mnemonic

            rates.append(rate)

        output = render_template('price.rates.html', rates=rates)
    return output
