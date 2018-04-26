"""
Asset Allocation module. To be replaced by Asset-Allocation package.
"""
from decimal import Decimal
from typing import List

try:
    import simplejson as json
except ImportError:
    import json
import os
from os import path
from piecash import Book, Commodity, Price
from gnucash_portfolio.accounts import AccountAggregate, AccountsAggregate
from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate
from gnucash_portfolio.currencies import CurrencyAggregate


class AssetBase:
    """Base class for asset group & class"""

    def __init__(self, json_node):
        self.data = json_node
        # reference to parent object
        self.parent: AssetClass = None

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

    @property
    def fullname(self):
        """ includes the full path with parent names """
        prefix = ""
        if self.parent:
            if self.parent.fullname:
                prefix = self.parent.fullname + ":"
        else:
            # Only the root does not have a parent. In that case we also don't need a name.
            return ""

        return prefix + self.name


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

        self.stocks: List[Stock] = []
        # parse stocks
        if "stocks" not in json_node:
            return

        for symbol in json_node["stocks"]:
            stock = Stock(symbol)
            # todo add asset class allocation for this security.
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
        # Parent class
        self.parent = None

    def __repr__(self):
        return f"<Stock (symbol='{self.symbol}')>"

    @property
    def value(self) -> Decimal:
        """Value of the shares. Value = Quantity * Price"""
        return self.quantity * self.price

    @property
    def asset_class(self) -> str:
        """ Returns the full asset class path for this stock """
        result = self.parent.name if self.parent else ""
        # Iterate to the top asset class and add names.
        cursor = self.parent
        while cursor:
            result = cursor.name + ":" + result
            cursor = cursor.parent
        return result


class _AllocationLoader:
    """ Parses the allocation settings and loads the current allocation from database """

    def __init__(self, currency: Commodity, book: Book):
        self.currency = currency
        self.book = book
        self.asset_allocation = None
        # Asset Class index populated during load, for performance.
        self.asset_class_index = {}

    def load_asset_allocation_model(self):
        """ Loads Asset Allocation model for display """
        self.asset_allocation = self.load_asset_allocation_config()
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

    def load_asset_allocation_config(self) -> AssetGroup:
        """ Loads only the configuration from json """
        # read asset allocation file
        root_node = self.__load_asset_allocation_config_json()
        result = self.__parse_node(root_node)
        return result

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
                    quantity = stock_svc.get_quantity()
                    stock.quantity = quantity

                    # last price
                    last_price: Price = stock_svc.get_last_available_price()
                    stock.price = last_price.value

                    # Value
                    stock_value = last_price.value * quantity
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

        svc = CurrencyAggregate(self.book, currency)
        last_price = svc.get_latest_rate(base_cur)

        result = value * last_price.value

        return result

    def get_cash_balance(self, root_account_name: str) -> Decimal:
        """ Loads investment cash balance in base currency """
        svc = AccountsAggregate(self.book)
        root_account = svc.get_by_fullname(root_account_name)
        acct_svc = AccountAggregate(self.book, root_account)
        result = acct_svc.get_cash_balance_with_children(root_account, self.currency)
        return result

    def __parse_node(self, node):
        """Creates an appropriate entity for the node. Recursive."""
        entity = None

        if "classes" in node:
            # Asset Class Group
            entity = AssetGroup(node)
            child_allocation_sum = Decimal(0)
            # Process child nodes
            for child_node in node["classes"]:
                # recursive call
                child = self.__parse_node(child_node)

                child.parent = entity
                # log(DEBUG, "adding %s as parent to %s", entity.name, child.name)
                entity.classes.append(child)
                child_allocation_sum += child.allocation

            # compare allocation to the sum of child allocations
            if entity.allocation != child_allocation_sum:
                raise ValueError("allocation does not match (self/child)",
                                 entity.allocation, child_allocation_sum)

        if "stocks" in node:
            # Asset Class
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

        # add asset class to index.
        self.asset_class_index[entity.name] = entity
        # log(DEBUG, "adding %s (%s) to asset class index", entity.name, entity.fullname)
        # log(DEBUG, "%s", self.asset_class_index)

        return entity

    def __load_asset_allocation_config_json(self):
        """
        Loads asset allocation from the file.
        Returns the list of asset classes.
        """
        allocation_file = path.abspath(path.join(
            os.path.dirname(os.path.realpath(__file__)), "../config/assetAllocation.json"))
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
            # child.curr_value = total * child.curr_alloc / 100
            child.value_diff = child.curr_value - child.alloc_value

            # Threshold
            child.over_threshold = abs(child.alloc_diff_perc) > self.asset_allocation.threshold

            self.__calculate_percentages(child, total)
        return


class AssetAllocationAggregate():
    """ No longer used!
    The main service class """

    def __init__(self, book: Book):
        self.book = book
        self.root: AssetGroup = None
        # index for asset classes
        self.__asset_class_index = None
        # index for stocks
        self.__stock_index: List[Stock] = None

    def load_full_model(self, currency: Commodity):
        """ Populates complete Asset Allocation tree """
        loader = _AllocationLoader(currency, self.book)
        return loader.load_asset_allocation_model()

    def load_config_only(self, currency: Commodity):
        """ Loads only the asset allocation tree from configuration """
        loader = _AllocationLoader(currency, self.book)
        config = loader.load_asset_allocation_config()
        # get the asset class index
        self.__asset_class_index = loader.asset_class_index
        return config

    def find_class_by_fullname(self, fullname: str):
        """ Locates the asset class by fullname. i.e. Equity:International """
        found = self.__get_by_fullname(self.root, fullname)
        return found

    def __get_by_fullname(self, asset_class, fullname: str):
        """ Recursive function """
        if asset_class.fullname == fullname:
            return asset_class

        if not hasattr(asset_class, "classes"):
            return None

        for child in asset_class.classes:
            found = self.__get_by_fullname(child, fullname)
            if found:
                return found

        return None

    def get_stock(self, symbol: str) -> List[Stock]:
        """ Finds all the stock allocations by symbol """
        # find this symbol
        instances = [self.stock_index[symbol] for index_symbol in self.stock_index if index_symbol == symbol]
        # log(DEBUG, "found %s instances for symbol %s", instances, symbol)
        return instances

    @property
    def asset_class_index(self) -> List[AssetClass]:
        """ Creates and returns an index of asset classes """
        if self.__asset_class_index:
            return self.__asset_class_index
        return self.__asset_class_index

    @property
    def stock_index(self):
        """ Creates index of all stock symbols in allocation """
        # iterate through allocation, get all the stocks, put them into index
        if self.__stock_index:
            return self.__stock_index
        index = {}

        # log(DEBUG, "starting with asset class index %s", self.asset_class_index)
        # create asset class index first.
        for name in self.asset_class_index:
            asset_class = self.asset_class_index[name]
            # log(DEBUG, "%s found in asset class index. Parent: %s",
            #     asset_class.name, asset_class.parent)

            if isinstance(asset_class, AssetGroup):
                continue
            # if not isinstance(asset_class, AssetClass):
            for stock in asset_class.stocks:
                symbol = stock.symbol
                # populate
                index[symbol] = stock
                # log(DEBUG, "adding %s to stock index", symbol)

        # log(DEBUG, "stock index complete: %s", index)
        self.__stock_index = index
        return self.__stock_index
