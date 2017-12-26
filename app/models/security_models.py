""" Models for Securities """

from typing import List
from piecash import Account, Commodity


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
        self.security: Commodity = None
        self.accounts: List[Account] = None
