"""
Imports security prices into GnuCash file.
Usage:
import_security_prices.py <pricefile>.csv

The csv file should contain the following:
symbol,price,date
AEF.AX,128.02,"10/11/2017"
"""
import sys
import os
from typing import List
from logging import log, INFO, DEBUG
from piecash import Commodity, Price
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib.csv_parser import CsvPriceParser

def import_file(filename):
    """
    Imports the commodity prices from the given .csv file.
    """
    #file_path = os.path.relpath(filename)
    file_path = os.path.abspath(filename)
    log(DEBUG, "Loading prices from %s", file_path)

    prices = __read_prices_from_file(file_path)
    with BookAggregate(for_writing=True) as svc:
        svc.prices.import_prices(prices)

        print("Saving book...")
        svc.book.save()

def __read_prices_from_file(file_path: str) -> List[Price]:
    # open file and read prices
    prices = []
    content = None

    with open(file_path, "r") as file_object:
        content = file_object.read()
    # file_object.close()

    # Currency is set later. It is taken from the stock currency info in db.
    parser = CsvPriceParser(currency=None)
    prices = parser.get_prices_from_csv(content)

    return prices

###############################################################################
def test():
    """ Test method, when run from console """
    currency_symbol = None
    filename = None
    if not len(sys.argv) > 1:
        #print("You must send the file name as the first argument.")
        #print("Using test file for demo.")
        #filename = "data/AUD_2017-11-11_142445.csv"
        filename = input("Please enter the filename to import: ")
        # check if it is a valid file
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            print(filename, "is not a valid file.")
            filename = None
            quit()

        currency_symbol = input("Currency for the prices: ")
    else:
        filename = sys.argv[1]
        currency_symbol = sys.argv[2]

    currency_symbol = currency_symbol.upper()

    if filename:
        import_file(filename)

if __name__ == "__main__":
    test()
