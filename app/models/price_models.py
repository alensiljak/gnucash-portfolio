""" Models for price actions """

class RateViewModel:
    """ View model for exchange rate """
    def __init__(self):
        self.date = None
        self.value = 0
        self.currency = ""
        self.base_currency = ""
