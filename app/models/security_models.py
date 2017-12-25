""" Models for Securities """

from typing import List
from piecash import Account, Commodity


#@dataclass
class StockAnalysisInputModel: #pylint: disable=invalid-name
    """ Input model for Stock Analysis """
    symbol: str = None


class SecurityDetailsViewModel:
    def __init__(self):
        self.security: Commodity = None
        self.accounts: List[Account] = None
