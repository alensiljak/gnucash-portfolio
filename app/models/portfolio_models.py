""" Models for Portfolio section """

from datetime import datetime
#from dataclasses import dataclass


#@dataclass
class PortfolioValueInputModel(): # pylint: disable=invalid-name
    """ Search model for Portfolio Value """
    as_of_date: datetime = datetime(datetime.today().year,
                                    datetime.today().month,
                                    datetime.today().day)
    stock: str = ""


#@dataclass
class PortfolioValueViewModel(): # pylint: disable=invalid-name
    """ View Model for portfolio value report """
    filter = None
    stock_rows = []
