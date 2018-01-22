""" Currency exchange rates import """

from logging import log, DEBUG
from decimal import Decimal
try: import simplejson as json
except ImportError: import json
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib.currencyrates import FixerioModelMapper
from gnucash_portfolio.lib import datetimeutils
from gnucash_portfolio.model.price_model import PriceModel


def test_parsing_fixerio_response():
    """ parse fixer.io response into an array of price models """
    response = '''{
        "base": "EUR",
        "date": "2017-12-29",
        "rates": {
            "AUD": 1.5346,
            "BGN": 1.9558,
            "BRL": 3.9729,
            "CAD": 1.5039,
            "CHF": 1.1702,
            "CNY": 7.8044,
            "CZK": 25.535,
            "DKK": 7.4449,
            "GBP": 0.88723,
            "HKD": 9.372,
            "HRK": 7.44,
            "HUF": 310.33,
            "IDR": 16239,
            "ILS": 4.1635,
            "INR": 76.606,
            "JPY": 135.01,
            "KRW": 1279.6,
            "MXN": 23.661,
            "MYR": 4.8536,
            "NOK": 9.8403,
            "NZD": 1.685,
            "PHP": 59.795,
            "PLN": 4.177,
            "RON": 4.6585,
            "RUB": 69.392,
            "SEK": 9.8438,
            "SGD": 1.6024,
            "THB": 39.121,
            "TRY": 4.5464,
            "USD": 1.1993,
            "ZAR": 14.805
        }
    }'''
    response_json = json.loads(response)

    importer = FixerioModelMapper()
    actual = importer.map_to_model(response_json)
    # log(DEBUG, actual)

    assert actual

    usd_price = next(price_model for price_model in actual if price_model.symbol == "USD")
    assert response_json["rates"]["USD"] == usd_price.value

def test_import_without_saving(svc_rw: BookAggregate):
    """ Test the import process without actuall saving to database """
    # Arrange
    aud = svc_rw.currencies.get_by_symbol("AUD")
    expected = 1
    today = datetimeutils.today()

    rates = []
    rates.append(PriceModel("AUD", "EUR", Decimal('0.63'), today))

    prices = aud.prices.all()
    assert not prices

    # Act

    svc_rw.currencies.import_fx_rates(rates)

    # Asserts

    prices = aud.prices.all()
    actual = len(prices)

    assert actual == expected
