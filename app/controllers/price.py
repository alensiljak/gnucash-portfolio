""" Price controller """
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate
from models.price_models import RateViewModel

price_controller = Blueprint('price_controller', __name__, url_prefix='/price')

@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')

@price_controller.route('/import')
def import_prices():
    """ Stock price import """
    return render_template('price.import.html')

@price_controller.route('/import', methods=['POST'])
def import_post():
    """ Imports the file """
    if 'import_file' not in request.files:
        return "No file selected"

    file_binary = request.files['import_file']
    if file_binary.content_type != "application/octet-stream":
        return "Wrong file type submitted"

    content = file_binary.read()
    file_binary.close()

    print(content)

    return render_template('incomplete.html')

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
