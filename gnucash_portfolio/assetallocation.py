"""
Asset Allocation module
"""
from decimal import Decimal
import json
import os
from os import path
from piecash import Book, Commodity, Price
from gnucash_portfolio.lib import generic, templates
from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate
from gnucash_portfolio.securityaggregate import SecurityAggregate, SecuritiesAggregate
from gnucash_portfolio.currencyaggregate import CurrencyAggregate


class AssetBase:
    """Base class for asset group & class"""
    def __init__(self, json_node):
        self.data = json_node

        # Set allocation %.
        self.allocation = Decimal(0)
        if "allocation" in json_node:
            self.allocation = Decimal(json_node["allocation"])
        else:
            self.allocation = Decimal(0)
        # How much is currently allocated, in %.
        self.curr_alloc = Decimal(0)
        # Difference between allocation and allocated.
        self.alloc_diff = Decimal(0)
        # Difference in percentages of allocation
        self.alloc_diff_perc = Decimal(0)

        # Current value in currency.
        self.alloc_value = Decimal(0)
        # Allocated value
        self.curr_value = Decimal(0)
        # Difference between allocation and allocated
        self.value_diff = Decimal(0)

        # Threshold. Expressed in %.
        self.threshold = Decimal(0)
        self.over_threshold = False
        self.under_threshold = False

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
        # For cash asset class
        self.root_account = None

        self.stocks: list(Stock) = []
        # parse stocks
        if "stocks" not in json_node:
            return

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
    def __init__(self, currency: Commodity, book: Book):
        self.currency = currency
        self.book = book
        self.asset_allocation = None

    def load_asset_allocation_model(self):
        """ Loads Asset Allocation model for display """
        # read asset allocation file
        root_node = self.__load_asset_allocation_config()
        self.asset_allocation = self.__parse_node(root_node)

        # Populate values from database.
        self.__load_values_into(self.asset_allocation)

        # calculate percentages
        total_value = self.asset_allocation.curr_value
        self.__calculate_percentages(self.asset_allocation, total_value)

        # Return model.
        model = {
            'allocation': self.asset_allocation,
            'currency': self.currency.mnemonic
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
                svc = SecuritiesAggregate(self.book)
                for stock in child.stocks:
                    # then, for each stock, calculate value
                    symbol = stock.symbol
                    cdty = svc.get_stock(symbol)
                    stock_svc = SecurityAggregate(self.book, cdty)

                    # Quantity
                    num_shares = stock_svc.get_num_shares()
                    stock.quantity = num_shares

                    # last price
                    last_price: Price = stock_svc.get_last_available_price()
                    stock.price = last_price.value

                    # Value
                    stock_value = last_price.value * num_shares
                    if last_price.currency != self.currency:
                        # Recalculate into the base currency.
                        stock_value = self.get_value_in_base_currency(
                            stock_value, last_price.currency)

                    child.curr_value += stock_value

            if child.name == "Cash":
                # load cash balances
                child.curr_value = self.get_cash_balance(child.root_account)

            asset_group.curr_value += child.curr_value

    def get_value_in_base_currency(self, value: Decimal, currency: Commodity) -> Decimal:
        """ Recalculates the given value into base currency """
        base_cur = self.currency
        svc = CurrencyAggregate(self.book)
        last_price = svc.get_latest_price(currency)

        result = value * last_price.value

        #print("recalculating", currency.mnemonic, value, "into", result, self.currency.mnemonic)
        return result

    def get_cash_balance(self, root_account_name: str) -> Decimal:
        """ Loads investment cash balance in base currency """
        svc = AccountsAggregate(self.book)
        root_account = svc.get_account_by_fullname(root_account_name)
        acct_svc = AccountAggregate(self.book, root_account)
        result = acct_svc.get_cash_balance_with_children(root_account, self.currency)
        return result

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

        # Cash
        if node["name"] == "Cash":
            # Cash node
            entity = AssetClass(node)
            entity.root_account = node["rootAccount"]

        # Threshold
        if "threshold" in node:
            threshold = node["threshold"].replace('%', '')
            entity.threshold = Decimal(threshold)

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

    def __calculate_percentages(self, asset_group: AssetGroup, total: Decimal):
        """ calculate the allocation percentages """
        if not hasattr(asset_group, "classes"):
            return

        for child in asset_group.classes:
            # calculate
            # allocation is read from the config.
            child.curr_alloc = child.curr_value * 100 / total
            child.alloc_diff = child.curr_alloc - child.allocation
            child.alloc_diff_perc = child.alloc_diff * 100 / child.allocation

            # Values
            child.alloc_value = total * child.allocation / 100
            # Value is calculated during load.
            #child.curr_value = total * child.curr_alloc / 100
            child.value_diff = child.curr_value - child.alloc_value

            # Threshold
            child.over_threshold = abs(child.alloc_diff_perc) > self.asset_allocation.threshold

            self.__calculate_percentages(child, total)
        return None
