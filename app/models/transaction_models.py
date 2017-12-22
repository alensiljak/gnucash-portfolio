""" Models for Transactions """

#from collections import namedtuple
from types import SimpleNamespace


# Input model for scheduled transactions list.
ScheduledTxSearchModel = SimpleNamespace( # pylint: disable=invalid-name
    'date_from',
    'date_to'
)


# result row for scheduled transactions.
SchedTxRowViewModel = SimpleNamespace( # pylint: disable=invalid-name
    'name',
    'start_date',
    'last_occurred'
)
