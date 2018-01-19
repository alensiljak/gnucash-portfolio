""" Price controller """
from logging import log, DEBUG
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib.csv_parser import CsvPriceParser
from app.models.price_models import (
    PriceImportViewModel, PriceImportInputModel, PriceImportSearchViewModel)
from app.models.generic_models import ValidationResult

price_controller = Blueprint( # pylint: disable=invalid-name
    'price_controller', __name__, url_prefix='/price')


@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')

@price_controller.route('/download/<path:symbol>')
def download(symbol):
    """ download the latest price for security """
    log(DEBUG, symbol)
    model = {
        "symbol": symbol
    }
    return render_template('price.download.html', model=model)

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
    input_model = __read_review_input_model()

    validation = __validate_review_input_model(input_model)
    if not validation.valid:
        return import_prices(validation.message)

    try:
        parser = CsvPriceParser(input_model.currency)
        prices = parser.parse_prices_from_file_stream(input_model.csv_file)
    except ValueError as value_error:
        return import_prices(value_error)

    # Display the prices for review.
    with BookAggregate() as svc:
        # View model
        ref = __load_search_reference_model(svc)

        model = PriceImportViewModel()
        model.filename = input_model.csv_file.filename
        model.prices = prices

        return render_template('price.import.confirm.html',
                               model=model, search=input_model, ref=ref)

@price_controller.route('/load', methods=['POST'])
def load_prices():
    """ Imports .csv prices into database. """
    # Read user input.
    input_model: PriceImportInputModel = __read_review_input_model()

    validation = __validate_review_input_model(input_model)
    if not validation.valid:
        return import_prices(validation.message)

    # Get prices from file.
    try:
        parser = CsvPriceParser(input_model.currency)
        prices = parser.parse_prices_from_file_stream(input_model.csv_file)
    except ValueError as value_error:
        return import_prices(value_error)

    # Import prices.
    with BookAggregate(for_writing=True) as svc:
        result = svc.prices.import_prices(prices)
        svc.save()

    with BookAggregate() as svc:
        model = PriceImportViewModel()
        model.filename = input_model.csv_file.filename
        model.prices = prices

        return render_template('price.import.result.html', model=model, result=result)

@price_controller.route('/for/<symbol>')
def prices_for_symbol(symbol):
    """ displays all prices for symbol """
    with BookAggregate() as svc:
        sec_agg = svc.securities.get_aggregate_for_symbol(symbol)
        prices = sec_agg.get_prices()
        model = {
            "symbol": symbol,
            "prices": prices
        }
        return render_template('security.prices.html', model=model)

###############################################
# Private

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
