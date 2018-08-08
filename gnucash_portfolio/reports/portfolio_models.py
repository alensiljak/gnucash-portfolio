""" Models for Portfolio section """

from datetime import datetime
from typing import List
#from dataclasses import dataclass
from gnucash_portfolio.model.stock_model import StockViewModel


#@dataclass
class PortfolioValueInputModel(): # pylint: disable=invalid-name
    """ Search model for Portfolio Value """
    def __init__(self):
        from pydatum import Datum

        today = Datum()
        today.today()

        self.as_of_date: datetime = today.value
        self.stock: str = ""


#@dataclass
class PortfolioValueViewModel(): # pylint: disable=invalid-name
    """ View Model for portfolio value report """
    def __init__(self):
        self.filter = None
        self.stock_rows: List[StockViewModel] = []
