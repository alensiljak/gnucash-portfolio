"""
Asset Allocation class
"""
#from enum import Enum
from decimal import Decimal
#from assetallocation import AssetClass, AssetGroup

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
        
        # Number of shares
        self.quantity = Decimal(0)
