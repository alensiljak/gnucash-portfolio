""" Split model """

class SplitModel:
    """ Allows modifications to the properties without saving them to the database """
    def __init__(self):
        self.account_guid = None
        self.memo = None
        self.quantity = None
        self.value = None
