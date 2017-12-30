""" Models for Asset Allocation """

from typing import List
from gnucash_portfolio.assetallocation import AssetGroup


class AssetGroupDetailsViewModel:
    """ view model for asset group details """
    def __init__(self):
        self.fullname = None
        # base currency display name
        self.base_currency = None
        self.asset_class: AssetGroup = None
        self.classes: List[AssetGroupChildDetailViewModel] = []
        self.stocks: List[AssetGroupChildDetailViewModel] = []

class AssetGroupChildDetailViewModel:
    """ Child element for asset group view model """
    def __init__(self):
        self.fullname = None
        self.name = None
        self.description = None
        self.value = None
        # Currency name
        self.currency = None
        # Value in base currency.
        self.value_base_cur = None
