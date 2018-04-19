""" Models for distributions report """

from datetime import datetime
from typing import List

from gnucash_portfolio.lib import datetimeutils


class DistributionsInputModel:
    """ User input / parameters """
    def __init__(self):
        self.period: str = datetimeutils.get_period_last_3_months()
        # value of the input field
        self.accounts: str = None
        self.currency = ""

    @property
    def date_from(self) -> datetime:
        """ extract from date """
        return datetimeutils.get_period_start(self.period)

    @property
    def date_to(self):
        """ extract from date """
        return datetimeutils.get_period_end(self.period)

    @property
    def accounts_list(self) -> List[str]:
        """ Parses user input and returns the list of entered accounts """
        return self.accounts.split(',')


class DistributionsViewModel:
    """ View model for distributions """
    def __init__(self):
        self.splits = []
