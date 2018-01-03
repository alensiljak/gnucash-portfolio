""" Models for Portfolio section """

from datetime import datetime
from gnucash_portfolio.lib import datetimeutils
#from dataclasses import dataclass


#@dataclass
class PortfolioValueInputModel(): # pylint: disable=invalid-name
    """ Search model for Portfolio Value """
    def __init__(self):
        self.as_of_date: datetime = datetimeutils.today_date()
        self.stock: str = ""


#@dataclass
class PortfolioValueViewModel(): # pylint: disable=invalid-name
    """ View Model for portfolio value report """
    def __init__(self):
        self.filter = None
        self.stock_rows = []
