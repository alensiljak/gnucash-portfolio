""" Models for Transactions """

#from collections import namedtuple
#from types import SimpleNamespace
from recordclass import recordclass


# Input model for scheduled transactions list.
ScheduledTxSearchModel = recordclass('ScheduledTxSearchModel', [
    ('date_from', None),
    ('date_to', None)
])


# result row for scheduled transactions.
SchedTxRowViewModel = recordclass("ScheduledTxSearchModel", [
    ('name', None),
    'start_date',
    'last_occurred'
])
