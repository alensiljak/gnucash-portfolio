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
from lib import Price
from lib import database
import csv

def import_file(filename):
    """
    Imports the commodity prices from the given .csv file.
    """
    file_path = os.path.relpath(filename)
    print("Loading prices from", file_path)

    prices = __read_prices_from_file(file_path)
    for price in prices:
        #print(price.name, price.date, price.currency, price.value)
        __import_price(price)

def __read_prices_from_file(file_path):
    # open file and read prices
    prices = []

    with open(file_path, "r") as file_object:
        reader = csv.reader(file_object)
        for row in reader:
            price = Price.Price()
            price.date = price.parse_euro_date(row[2])
            price.name = row[0]
            price.value = price.parse_value(row[1])
            #price.currency = "EUR"

            prices.append(price)
            #print(', '.join(row))
    # file_content = file_object.read()
    # file_object.close()

    # return list of prices
    return prices

def __import_price(price):
    # import individual price
    db = database.Database()
    with db.open_book(for_writing=True) as book:
        security = book.commodities.get(mnemonic=price.name)
        print(security)
    return

###############################################################################
if __name__ == "__main__":
    filename = None
    if not len(sys.argv) > 1:
        print("You must send the file name as the first argument.")
        print("Using test file for demo.")
        filename = "data/AUD_2017-11-11_142445.csv"
    else:
        filename = sys.argv[1]

    import_file(filename)
    