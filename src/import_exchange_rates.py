"""
Import currency exchange rates from .csv file into GnuCash
"""
#from pprint import pprint
import database
import settings
from piecash import Commodity

def test():
    print("yo")

def load_rates():
    # todo: load rates from .csv
    return ['rate1', 'rate2']

def main():
    currencies = settings.get_currencies()
    # "currencies: " + 
    print(currencies)

    # todo: load the rates from the file
    rates = load_rates()
    # todo: iterate over rates and import for specified currencies only.
    for rate in rates:
        print(rate)

with database.open_book() as book:
    # do something
    test()
    main()
    