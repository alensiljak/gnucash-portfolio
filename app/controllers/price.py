""" Price controller """
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate, CurrenciesAggregate
from gnucash_portfolio.pricesaggregate import PricesAggregate
from models.price_models import RateViewModel, PriceImportViewModel, PriceImportFormViewModel

price_controller = Blueprint('price_controller', __name__, url_prefix='/price')

@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')

@price_controller.route('/import')
def import_prices(message: str = None):
    """ Stock price import """
    model = {}
    if message:
        model["message"] = message

    with BookAggregate() as svc:
        search = __load_search_reference_model(svc)

        return render_template('price.import.html', model=model, search=search)

@price_controller.route('/import', methods=['POST'])
def import_post():
    """ Imports the prices file (.csv) """
    file_binary = request.files['import_file']
    message = None
    if not file_binary:
        message = "No file selected"
    if file_binary.content_type != "application/octet-stream":
        message = "Wrong file type submitted"

    content = file_binary.read().decode("utf-8")
    if not content:
        message = "The file is empty!"

    if message:
        return import_prices(message)

    file_binary.close()

    with BookAggregate() as svc:
        # TODO import prices. Redo the module for import.
        prices_svc = PricesAggregate(svc.book)
        prices = prices_svc.get_prices_from_csv(content)
        print(prices)

        # View model
        search = __load_search_reference_model(svc)

        model = PriceImportViewModel()
        model.filename = file_binary.name

        return render_template('price.import.result.html', model=model, search=search)

@price_controller.route('/importapproved', methods=['POST'])
def import_prices_accept():
    """ The import of prices after user confirms """

def __load_search_reference_model(svc: BookAggregate):
    """ Populates the reference data for the search form """
    model = PriceImportFormViewModel()

    #cur_svc = CurrenciesAggregate(svc.book)
    model.currencies = svc.book.currencies

    return model

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
