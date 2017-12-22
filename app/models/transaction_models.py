""" Models for Transactions """

#from collections import namedtuple
from types import SimpleNamespace


# Input model for scheduled transactions list.
ScheduledTxSearchModel = SimpleNamespace( # pylint: disable=invalid-name
    date_from=None,
    date_to=None
)


# result row for scheduled transactions.
SchedTxRowViewModel = SimpleNamespace( # pylint: disable=invalid-name
    name=None,
    start_date=None,
    last_occurred=None
)
