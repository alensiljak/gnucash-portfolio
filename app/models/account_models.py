""" Models for account views """

from decimal import Decimal


class AccountTransactionsViewModel:
    """ View model for account transactions """
    def __init__(self):
        self.start_balance = Decimal(0)
        self.splits = []
        self.end_balance = Decimal(0)


class AccountTransactionsInputModel:
    """ User input """
    def __init__(self):
        # Account id
        self.account_id: str = None
        # Date range
        self.period: str = None


class AccountTransactionsRefModel:
    """ Reference model for search """
    def __init__(self):
        # Dictionary of account id/fullnames.
        self.accounts = {}

class AccountDetailsViewModel:
    """ View model for account details """
    def __init__(self):
        self.account = None
