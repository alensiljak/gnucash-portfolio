""" Models for Securities """

from decimal import Decimal
from typing import List
from piecash import Account, Commodity, Price


#@dataclass
class StockAnalysisInputModel: #pylint: disable=invalid-name
    """ Input model for Stock Analysis """
    def __init__(self):
        self.symbol: str = None


class SecurityAnalysisRefModel:
    """ Reference data for input form """
    def __init__(self):
        self.securities = []


class SecurityDetailsViewModel:
    def __init__(self):
        self.symbol = None
        self.security: Commodity = None
        self.quantity: Decimal = Decimal(0)
        self.price: Price = None
        self.value: Decimal = None
        self.currency: str = None
        # Total amount paid in currency. Used for calculation of the average price.
        self.total_paid: Decimal = None
        # Average price paid per unit.
        self.average_price: Decimal = None

        self.accounts: List[Account] = None
        self.income_accounts: List[Account] = None
