""" Stock model """

#from dataclasses import dataclass
from decimal import Decimal
from typing import List
from piecash import Account, Commodity, Price


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


class SecurityDetailsViewModel:
    """ Security Details """
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
        # Unrealized Profit/Loss
        self.profit_loss = None
        self.profit_loss_perc = None
        # Income amount in currency
        self.income = None
        self.income_perc = None
        # Income % for the last 12 months
        self.income_perc_last_12m = None
        # Total return = value diff + income
        self.total_return = None
        self.total_return_perc = None

        self.accounts: List[Account] = None
        self.income_accounts: List[Account] = None
        # List of asset classes the security belongs to.
        self.asset_classes = []
