""" Models for price actions """

#from dataclasses import dataclass
from decimal import Decimal
from typing import List
from piecash import Price


#@dataclass
class RateViewModel:
    """ View model for exchange rate """
    def __init__(self):
        self.date = None
        self.value: Decimal = 0
        self.currency = ""
        self.base_currency = ""


#@dataclass
class PriceImportViewModel:
    """ Price import results """
    def __init__(self):
        self.filename: str = None
        self.prices: List[Price] = []


#@dataclass
class PriceImportInputModel:
    """ Static model for the import form """
    def __init__(self):
        self.currency = None
        self.csv_file = None


class PriceImportSearchViewModel:
    """ For displaying reference data on the search form """
    def __init__(self):
        self.currencies = []
