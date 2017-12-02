"""
Asset Allocation class
"""
from enum import Enum

class AssetAllocation:
    """The root object"""
    classes = []

    def __init__(self):
        """
        Constructor
        """

    def test():
        print("yo")

class AssetGroup:
    """Group contains other groups or asset classes"""
    name = None
    allocation = 0
    classes = []

    def __init__(self, json_node):
        self.name = json_node["name"]
        self.allocation = json_node["allocation"]

class AssetClass:
    """Asset Class contains stocks"""
    name = None
    allocation = 0
    stocks = []

    def __init__(self, json_node):
        self.name = json_node["name"]
        self.allocation = json_node["allocation"]

class Stock:
    """Stock link"""
    symbol = None

    def __init__(self, symbol: str):
        """Parse json node"""
        self.symbol = symbol

class NodeType(Enum):
    GROUP = 1
    ASSETCLASS = 2
    STOCK = 3