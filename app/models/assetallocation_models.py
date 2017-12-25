""" Models for Asset Allocation """

from gnucash_portfolio.assetallocation import AssetGroup


class AssetGroupDetailsViewModel:
    """ view model for asset group details """
    def __init__(self):
        self.fullname = None
        self.asseallocation: AssetGroup = None
