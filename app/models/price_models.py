""" Models for price actions """

#from dataclasses import dataclass
from decimal import Decimal


#@dataclass
class RateViewModel: # pylint: disable=invalid-name
    """ View model for exchange rate """
    date = None
    value: Decimal = 0
    currency = ""
    base_currency = ""


#@dataclass
class PriceImportViewModel: # pylint: disable=invalid-name
    """ Price import results """
    filename: str = None


#@dataclass
class PriceImportFormViewModel: # pylint: disable=invalid-name
    """ Static model for the import form """
    currencies = []
