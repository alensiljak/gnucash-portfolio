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
from piecash import Commodity, Price, Book
from sqlalchemy import func, or_
from gnucash_portfolio.lib import database, price as pricelib
from gnucash_portfolio.pricesaggregate import PricesAggregate

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

def __read_prices_from_file(file_path: str) -> List[Price]:
    # open file and read prices
    prices = []
    content = None

    with open(file_path, "r") as file_object:
        content = file_object.read()
    # file_object.close()

    svc = PricesAggregate(None)
    prices = svc.get_prices_from_csv(content)

    # return list of prices
    return prices

def __import_price(book: Book, price):
    """
    Import individual price
    """
    stock = __get_commodity(book, price.name)
    if stock is None:
        return

    # check if there is already a price for the date
    exists = stock.prices.filter(Price.date == price.date).all()
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
    symbol_only = symbol.split(".")[0]

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

def __create_price_for(commodity: Commodity, price):
    """
    Creates a new Price entry in the book, for the given commodity.
    """
    print("Adding a new price for", commodity.mnemonic, price.date.strftime("%Y-%m-%d"), 
        price.value)

    #currency = __get_stock_currency(commodity)
    currency = __get_currency(commodity.book, commodity.mnemonic)

    new_price = Price(commodity, currency, price.date, price.value)
    commodity.prices.append(new_price)


def __get_stock_currency(stock: Commodity) -> Commodity:
    """
    Reads the currency from the first available price information,
    assuming that all the prices are in the same currency for any symbol.
    """
    first_price = stock.prices.first()
    if not first_price:
        raise AssertionError("Price not found for", stock.mnemonic)

    return first_price.currency

def __get_currency(book: Book, symbol: str) -> Commodity:
    """
    Use the same currency for one file.
    """
    cur = book.currencies.get(mnemonic=symbol)
    #print("Using currency - ", cur.mnemonic)
    return cur

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
