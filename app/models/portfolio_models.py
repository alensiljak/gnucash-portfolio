""" Models for Portfolio section """

from datetime import datetime
#from types import SimpleNamespace
from typing import NamedTuple


class PortfolioValueInputModel(NamedTuple): # pylint: disable=invalid-name
    """ Search model for Portfolio Value """
    as_of_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    stock = ""


class PortfolioValueViewModel(NamedTuple): # pylint: disable=invalid-name
    """ View Model for portfolio value report """
    filter = None
    stock_rows = []
