""" Models for account views """

class AccountTransactionsViewModel:
    """ View model for account transactions """
    def __init__(self):
        self.splits = []


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
