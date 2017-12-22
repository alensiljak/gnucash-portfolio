""" Models for Portfolio section """

from datetime import datetime
from recordclass import recordclass


# """ Input model for portfolio value filter parameters """
PortfolioValueInputModel = recordclass("PortfolioValueInputModel", [
    ("as_of_date", datetime(datetime.today().year, datetime.today().month, datetime.today().day)),
    "stock"
])

    # def __init__(self):
    #     today = datetime.today()
    #     self.as_of_date: datetime = datetime(today.year, today.month, today.day)
    #     self.stock = ""

class PortfolioValueViewModel:
    """ View Model for portfolio value report """
    def __init__(self):
        self.filter = None
        self.stock_rows = []
