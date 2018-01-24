""" Models for price actions """

#from dataclasses import dataclass
from typing import List
from piecash import Price


# class PriceModel:
#     """ Model for Price, in order not to mess up the database """
#     def __init__(self, price: Price):
#         self.commodity_guid = price.commodity_guid
#         self.currency_guid = price.currency_guid
#         self.date = price.date
#         self.source = price.source
#         self.type = price.type
#         self.value = price.value

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
