""" Stock model """

#from dataclasses import dataclass
from decimal import Decimal


#@dataclass
class StockViewModel:
    """ View model for stock symbol """
    symbol: str = None
    exchange = None
    shares_num: Decimal = Decimal(0)
    avg_price = None
    price: Decimal = None
    currency = None
    cost = None
    balance = Decimal(0)
    gain_loss = None
    gain_loss_perc = None
    income: Decimal = None
