""" Models for Asset Allocation """

from typing import List
from gnucash_portfolio.assetallocation import AssetGroup


class AssetGroupDetailsViewModel:
    """ view model for asset group details """
    def __init__(self):
        self.fullname = None
        self.asset_class: AssetGroup = None
        self.classes: List[AssetGroupChildDetailViewModel] = []
        self.stocks: List[AssetGroupChildDetailViewModel] = []

class AssetGroupChildDetailViewModel:
    """ Child element for asset group view model """
    def __init__(self):
        self.fullname = None
        self.name = None
        self.value = None
