""" Models for price actions """
from types import SimpleNamespace


# """ View model for exchange rate """
RateViewModel = SimpleNamespace( # pylint: disable=invalid-name
    date=None,
    value=0,
    currency="",
    base_currency=""
)

# """ Price import results """
PriceImportViewModel = SimpleNamespace( # pylint: disable=invalid-name
    foo="bar",
    filename=None
)

#     """ Static model for the import form """
PriceImportFormViewModel = SimpleNamespace( # pylint: disable=invalid-name
    currencies=[]
)
