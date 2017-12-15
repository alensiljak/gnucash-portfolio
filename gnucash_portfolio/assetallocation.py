"""
Asset Allocation module
"""
from decimal import Decimal
import json
import os
from os import path
from piecash import Book, Price
from gnucash_portfolio.lib import generic, templates
from gnucash_portfolio.securityaggregate import StockAggregate

class AssetBase:
    """Base class for asset group & class"""
    def __init__(self, json_node):
        self.data = json_node

        self.value = Decimal(0)

        if "allocation" in json_node:
            self.allocation = Decimal(json_node["allocation"])
        else:
            self.allocation = Decimal(0)

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

class AllocationLoader:
    """ Parses the allocation settings and loads the current allocation from database """
    def __init__(self, currency_symbol: str):
        self.currency_symbol = currency_symbol
        self.book = None

    def load_asset_allocation_model(self, book: Book):
        """ Loads Asset Allocation model for display """
        self.book = book

        # read asset allocation file
        root_node = self.__load_asset_allocation_config()
        asset_allocation = self.__parse_node(root_node)

        # Populate values from database.
        self.__load_values_into(asset_allocation)

        model = {
            'allocation': asset_allocation
        }

        return model

    def __load_values_into(self, asset_group: AssetGroup):
        """
        Populates the asset class values from the database.
        Reads the stock values and fills the asset classes.
        """
        # iterate recursively until an Asset Class is found.
        for child in asset_group.classes:
            if isinstance(child, AssetGroup):
                self.__load_values_into(child)

            if isinstance(child, AssetClass):
                # Add all the stock values.
                svc = StockAggregate(self.book)
                for stock in child.stocks:
                    # then, for each stock, calculate value
                    symbol = stock.symbol
                    cdty = svc.get_stock(symbol)

                    # Quantity
                    num_shares = svc.get_number_of_shares(cdty)
                    stock.quantity = num_shares

                    # last price
                    last_price: Price = svc.get_last_available_price(cdty)
                    stock.price = last_price.value

                    stock_value = last_price.value * num_shares
                    child.value += stock_value

            asset_group.value += child.value


    def __parse_node(self, node):
        """Creates an appropriate entity for the node. Recursive."""
        entity = None

        if "classes" in node:
            entity = AssetGroup(node)
            # Process child nodes
            for child_node in node["classes"]:
                child = self.__parse_node(child_node)
                #allocation_sum +=
                entity.classes.append(child)

        if "stocks" in node:
            # This is an Asset Class
            entity = AssetClass(node)

        return entity


    def __load_asset_allocation_config(self):
        """
        Loads asset allocation from the file.
        Returns the list of asset classes.
        """
        allocation_file = path.abspath(path.join(os.path.dirname(os.path.realpath(__file__)), "../config/assetAllocation.json"))
        with open(allocation_file, 'r') as json_file:
            allocation_json = json.load(json_file)

        return allocation_json
