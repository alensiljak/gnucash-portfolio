""" Price controller """
#from logging import log, DEBUG
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate
from gnucash_portfolio.pricesaggregate import PricesAggregate
from app.models.price_models import RateViewModel, PriceImportViewModel, PriceImportSearchModel

price_controller = Blueprint( # pylint: disable=invalid-name
    'price_controller', __name__, url_prefix='/price')


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


@price_controller.route('/review', methods=['POST'])
def import_post():
    """ Imports the prices file (.csv) """
    input_model = __read_load_input_model()
    file_binary = input_model.csv_file

    if not file_binary:
        return import_prices("No file selected")
    if file_binary.content_type != "application/octet-stream":
        return import_prices("Wrong file type submitted")

    assert file_binary.filename != ''

    # Read file into lines for CSV processing.
    content = file_binary.read().decode("utf-8")
    #content = file_binary.readlines()
    if not content:
        return import_prices("The file is empty!")
    file_binary.close()

    with BookAggregate() as svc:
        # Display the prices for confirmation.
        prices_svc = PricesAggregate(svc.book)
        prices = prices_svc.get_prices_from_csv(content)
        # add the currency
        for price in prices:
            price.currency = request.form.get("search.currency")

        # View model
        search = __load_search_reference_model(svc)

        model = PriceImportViewModel()
        model.filename = file_binary.filename
        model.prices = prices

        return render_template('price.import.confirm.html', model=model, search=search)


def __read_load_input_model() -> PriceImportSearchModel:
    """ Read input model on price load """
    result = PriceImportSearchModel()

    result.csv_file = request.files['import_file']

    return result


@price_controller.route('/importapproved', methods=['POST'])
def import_prices_accept():
    """ The import of prices after user confirms """
    # TODO Import prices. Redo the module for import.
    return render_template('incomplete.html')


def __load_search_reference_model(svc: BookAggregate):
    """ Populates the reference data for the search form """
    model = PriceImportSearchModel()

    #cur_svc = CurrenciesAggregate(svc.book)
    model.currencies = svc.currencies.get_book_currencies()

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
            cur_svc = CurrencyAggregate(book_svc.book, cur)
            price = cur_svc.get_latest_price()
            if price:
                rate.date = price.date
                rate.value = price.value
                #print(price.commodity.mnemonic)
                rate.base_currency = price.currency.mnemonic

            rates.append(rate)

        output = render_template('price.rates.html', rates=rates)
    return output
