""" Price controller """
#from logging import log, DEBUG
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate
#from gnucash_portfolio.pricesaggregate import PricesAggregate
from gnucash_portfolio.lib import csv_parser
from app.models.price_models import (
    RateViewModel, PriceImportViewModel, PriceImportInputModel, PriceImportSearchViewModel)
from app.models.generic_models import ValidationResult


price_controller = Blueprint( # pylint: disable=invalid-name
    'price_controller', __name__, url_prefix='/price')


@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')


@price_controller.route('/import')
def import_prices(message: str = None):
    """ Stock price import. Data input. """
    model = {}
    if message:
        model["message"] = message

    with BookAggregate() as svc:
        ref = __load_search_reference_model(svc)
        search = None

        return render_template('price.import.html', model=model, search=search, ref=ref)


@price_controller.route('/review', methods=['POST'])
def import_post():
    """ Review the prices from the uploaded file (.csv) """
    input_model: PriceImportInputModel = __read_review_input_model()

    validation = __validate_review_input_model(input_model)
    if not validation.valid:
        return import_prices(validation.message)

    # Read file into lines for CSV processing.
    # noinspection PyBroadException
    try:
        prices = csv_parser.parse_prices_from_file_stream(input_model.csv_file)
    except ValueError as value_error:
        return import_prices(value_error)

    # Display the prices for review.
    with BookAggregate() as svc:
        #prices_svc = PricesAggregate(svc.book)

        # add the currency
        for price in prices:
            price.currency = input_model.currency

        # View model
        ref = __load_search_reference_model(svc)

        model = PriceImportViewModel()
        model.filename = input_model.csv_file.filename
        model.prices = prices

        return render_template('price.import.confirm.html',
                               model=model, search=input_model, ref=ref)


@price_controller.route('/load', methods=['POST'])
def load_prices():
    """ Imports .csv prices. """
    input_model: PriceImportInputModel = __read_review_input_model()

    validation = __validate_review_input_model(input_model)
    if not validation.valid:
        return import_prices(validation.message)

    # TODO Import prices. Redo the module for import.
    return render_template('incomplete.html')


def __read_review_input_model() -> PriceImportInputModel:
    """ Read input model on price load """
    result = PriceImportInputModel()

    result.currency = request.form.get("search.currency")
    result.csv_file = request.files['import_file']

    return result


def __validate_review_input_model(model: PriceImportInputModel):
    """ Validates user input """
    result = ValidationResult()
    result.valid = False

    file = model.csv_file
    if not file:
        result.message = "No file selected"
        return result

    if file.content_type != "application/octet-stream":
        result.message = "Wrong file type submitted"
        return result

    assert file.filename != ''

    # Validation passed.
    result.valid = True
    return result


def __load_search_reference_model(svc: BookAggregate) -> PriceImportSearchViewModel:
    """ Populates the reference data for the search form """
    model = PriceImportSearchViewModel()

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
