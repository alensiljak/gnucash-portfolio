""" Models for price actions """

#from dataclasses import dataclass
from typing import List
from piecash import Price


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
