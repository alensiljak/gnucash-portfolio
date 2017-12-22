""" Models for price actions """


class RateViewModel:
    """ View model for exchange rate """
    def __init__(self):
        self.date = None
        self.value = 0
        self.currency = ""
        self.base_currency = ""


class PriceImportViewModel:
    """ Price import results """
    def __init__(self):
        self.foo = "bar"
        self.filename = None

class PriceImportFormViewModel:
    """ Static model for the import form """
    def __init__(self):
        self.currencies = []
