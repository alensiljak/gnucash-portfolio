""" Stock model """

#from dataclasses import dataclass
from decimal import Decimal


#@dataclass
class StockViewModel:
    """ View model for stock symbol """
    symbol: str = None
    exchange: str = None
    shares_num: Decimal = Decimal(0)
    avg_price: Decimal = None
    price: Decimal = None
    currency: str = None
    cost = None
    balance = Decimal(0)
    gain_loss = None
    gain_loss_perc = None
    income: Decimal = None

    def __repr__(self):
        result = f"<StockViewModel {self.exchange}:{self.symbol},{self.shares_num:,} @ "
        result += f"{self.avg_price:,.2f} {self.currency}"
        result += ">"
        return result