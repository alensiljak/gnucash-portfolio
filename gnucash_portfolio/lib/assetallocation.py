"""
Asset Allocation module
"""
from decimal import Decimal
import json
import os
from os import path
from gnucash_portfolio import security_analysis
from gnucash_portfolio.lib import generic, templates, database

class AssetBase:
    """Base class for asset group & class"""
    data = None
    allocation = 0

    def __init__(self, json_node):
        self.data = json_node
        if "allocation" in json_node:
            self.allocation = Decimal(json_node["allocation"])

    @property
    def name(self):
        """Group name"""
        if not self.data:
            return ""

        if "name" in self.data:
            return self.data["name"]
        else:
            return ""


class AssetGroup(AssetBase):
    """Group contains other groups or asset classes"""

    def __init__(self, json_node):
        super().__init__(json_node)
        self.classes = []


class AssetClass(AssetBase):
    """Asset Class contains stocks"""

    def __init__(self, json_node):
        super().__init__(json_node)

        self.stocks: list(Stock) = []
        # parse stocks
        for symbol in json_node["stocks"]:
            stock = Stock(symbol)
            self.stocks.append(stock)


class Stock:
    """Stock link"""

    def __init__(self, symbol: str):
        """Parse json node"""
        self.symbol = symbol
        
        # Quantity (number of shares)
        self.quantity = Decimal(0)

        # Price (last known)
        self.price = Decimal(0)

    @property
    def value(self):
        """Value of the shares. Value = Quantity * Price"""
        return self.quantity * self.price


###################################

def load_asset_allocation_model(book_url: str):
    # read asset allocation file
    root_node = __load_asset_allocation_config()
    aa = __parse_node(root_node)

    # TODO calculate allocation in the book.
    # TODO add all the stock values.

    # load security information from the book.
    with database.Database(book_url).open_book() as book:
        __add_values(book, aa)

    model = {}
    model["allocation"] = aa

    return model

def __add_values(book, aa: AssetGroup):
    """
    Populates the asset class values from the database.
    Reads the stock values and fills the asset classes.
    """
    # iterate recursively until an Asset Class is found.
    for child in aa.classes:
        if isinstance(child, AssetGroup):
            __add_values(book, child)

        if isinstance(child, AssetClass):
            for stock in child.stocks:
                # then, for each stock, load information
                symbol = stock.symbol
                cdty = security_analysis.get_stock(book, symbol)

                # Quantity
                num_shares = security_analysis.get_number_of_shares(cdty)
                stock.quantity = num_shares

                # last price
                last_price = security_analysis.get_last_available_price(cdty)
                stock.price = last_price


def __parse_node(node):
    """Creates an appropriate entity for the node. Recursive."""
    entity = None

    if "classes" in node:
        entity = AssetGroup(node)
        # Process child nodes
        for child_node in node["classes"]:
            child = __parse_node(child_node)
            #allocation_sum +=
            entity.classes.append(child)

    if "stocks" in node:
        # This is an Asset Class
        entity = AssetClass(node)

    return entity


def __load_asset_allocation_config():
    """
    Loads asset allocation from the file.
    Returns the list of asset classes.
    """
    allocation_file = path.abspath(path.join(os.path.dirname(os.path.realpath(__file__)), "../data/assetAllocation.json"))
    with open(allocation_file, 'r') as json_file:
        allocation_json = json.load(json_file)

    return allocation_json
