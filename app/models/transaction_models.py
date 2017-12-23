""" Models for Transactions """

#from dataclasses import dataclass


#@dataclass
class ScheduledTxSearchModel: # pylint: disable=invalid-name
    """ Input model for scheduled transactions list """
    date_from = None
    date_to = None


#@dataclass
class SchedTxRowViewModel: # pylint: disable=invalid-name
    """ result row for scheduled transactions """
    name = None
    start_date = None
    last_occurred = None
