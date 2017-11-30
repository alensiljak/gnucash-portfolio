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
import csv
import piecash
from piecash import Commodity
from sqlalchemy import func, or_
#import piecash
from gnucash_portfolio.lib import database, price as pricelib

def import_file(filename):
    """
    Imports the commodity prices from the given .csv file.
    """
    #file_path = os.path.relpath(filename)
    file_path = os.path.abspath(filename)
    print("Loading prices from", file_path)

    prices = __read_prices_from_file(file_path)
    db = database.Database()
    with db.open_book(for_writing=True) as book:
        for price in prices:
            #print(price.name, price.date, price.currency, price.value)
            __import_price(book, price)
        
        print("Saving book...")
        book.save()

def __read_prices_from_file(file_path):
    # open file and read prices
    prices = []

    with open(file_path, "r") as file_object:
        reader = csv.reader(file_object)
        for row in reader:
            price = pricelib.Price()
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
    if stock is None:
        return

    # check if there is already a price for the date
    exists = stock.prices.filter(piecash.Price.date == price.date).all()
    if not exists:
        # Create new price for the commodity (symbol).
        __create_price_for(stock, price)
    else:
        print("price already exists for", stock.mnemonic, price.date.strftime("%Y-%m-%d"))
        existing_price = exists[0]
        # update price
        existing_price.value = price.value

def __get_commodity(book, symbol):
    """
    Loads the stock from the book.
    """
    #temp = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY").first()
    #print(temp.namespace, temp.mnemonic, temp.fullname, temp.cusip, temp.fraction)

    symbol_only = symbol.split(".")[0]

    #security = book.commodities(namespace="CURRENCY").get(mnemonic=price.name)
    #security = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY", func.lower(Commodity.mnemonic) == func.lower(price.name)).first()
    securities = book.session.query(Commodity).filter(Commodity.namespace != "template", Commodity.namespace != "CURRENCY", or_(Commodity.mnemonic.ilike(symbol_only), Commodity.mnemonic.ilike(symbol))).all()

    security = None

    if len(securities) == 0:
        print("Could not find", symbol_only)
        return None
    if len(securities) > 1:
        raise ValueError("More than one commodity found for", symbol)

    #if len(securities) == 1:
    security = securities[0]
    #print("Security", symbol, security)
    return security

def __create_price_for(commodity, price):
    """
    Creates a new Price entry in the book, for the given commodity.
    """
    print("Adding a new price for", commodity.mnemonic, price.date.strftime("%Y-%m-%d"), price.value)

    #currency = __get_stock_currency(commodity)
    currency = __get_currency(commodity.book)

    new_price = piecash.Price(commodity, currency, price.date, price.value)
    commodity.prices.append(new_price)
    #print(record.currency)

def __get_stock_currency(stock):
    """
    Reads the currency from the first available price information,
    assuming that all the prices are in the same currency for any symbol.
    """
    first_price = stock.prices.first()
    if not first_price:
        raise AssertionError("Price not found for", stock.mnemonic)

    return first_price.currency

def __get_currency(book):
    """
    Use the same currency for one file.
    """
    cur = book.currencies.get(mnemonic=currency_symbol)
    #print("Using currency - ", cur.mnemonic)
    return cur

###############################################################################
currency_symbol = None

if __name__ == "__main__":
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
    