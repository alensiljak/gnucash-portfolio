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
import lib
#from lib import Price
#from lib import database
import csv
import piecash
from piecash import Commodity
from sqlalchemy import func, or_
#import piecash

def import_file(filename):
    """
    Imports the commodity prices from the given .csv file.
    """
    file_path = os.path.relpath(filename)
    print("Loading prices from", file_path)

    prices = __read_prices_from_file(file_path)
    db = lib.database.Database()
    with db.open_book(for_writing=False) as book:
        for price in prices:
            #print(price.name, price.date, price.currency, price.value)
            __import_price(book, price)

def __read_prices_from_file(file_path):
    # open file and read prices
    prices = []

    with open(file_path, "r") as file_object:
        reader = csv.reader(file_object)
        for row in reader:
            price = lib.Price.Price()
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

def __import_price(book, price):
    """
    Import individual price
    """
    stock = __get_commodity(book, price.name)
    price = None

    # check if there is already a price for the date
    exists = stock.prices.filter(piecash.Price.date == price.date).all()
    if not exists:
        # todo create price for the commodity
        print("here we would create a new price for", price.name)
        price = None
    else:
        print("price already exists for", stock)
        price = exists.first

def __get_commodity(book, symbol):
    #temp = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY").first()
    #print(temp.namespace, temp.mnemonic, temp.fullname, temp.cusip, temp.fraction)

    symbol_only = symbol.split(".")[0]

    #security = book.commodities(namespace="CURRENCY").get(mnemonic=price.name)
    #security = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY", func.lower(Commodity.mnemonic) == func.lower(price.name)).first()
    securities = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY", or_(Commodity.mnemonic.ilike(symbol_only), Commodity.mnemonic.ilike(symbol))).all()
    if len(securities) > 1:
        raise ValueError("More than one commodity found for", symbol)
    
    security = securities[0]
    print("Security", symbol, security)
    return security

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
    