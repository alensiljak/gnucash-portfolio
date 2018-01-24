""" Split mapper """

from piecash import Split
from gnucash_portfolio.model.split_model import SplitModel

class SplitMapper:

    def map_split(self, split: Split, model: SplitModel):
        model.account_guid = split.account_guid
        model.memo = split.memo
        model.quantity = split.quantity
        model.value = split.value

        return model
