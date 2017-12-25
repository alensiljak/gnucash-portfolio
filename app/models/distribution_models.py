""" Models for distributions report """

from gnucash_portfolio.lib import datetimeutils


class DistributionsInputModel:
    """ User input / parameters """
    def __init__(self):
        self.period: str = None
        self.accounts = []
        self.currency = None

    @property
    def date_from(self):
        """ extract from date """
        return datetimeutils.get_from(self.period)

    @property
    def date_to(self):
        """ extract from date """
        return datetimeutils.get_to(self.period)


class DistributionsViewModel:
    """ View model for distributions """
    def __init__(self):
        self.splits = []
