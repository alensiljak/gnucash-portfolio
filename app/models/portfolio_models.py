""" Models for Portfolio section """

from datetime import datetime
from types import SimpleNamespace


PortfolioValueInputModel = SimpleNamespace( # pylint: disable=invalid-name
    as_of_date=datetime(datetime.today().year, datetime.today().month, datetime.today().day),
    stock=""
)

#""" View Model for portfolio value report """
PortfolioValueViewModel = SimpleNamespace( # pylint: disable=invalid-name
    filter=None,
    stock_rows=[]
)
