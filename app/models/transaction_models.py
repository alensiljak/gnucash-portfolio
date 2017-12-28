""" Models for Transactions """

#from dataclasses import dataclass
from gnucash_portfolio.lib import datetimeutils


#@dataclass
class ScheduledTxInputModel: # pylint: disable=invalid-name
    """ Input model for scheduled transactions list """
    def __init__(self):
        self.period_str = datetimeutils.get_period_last_week()

    @property
    def start_date(self):
        """ parses the period and returns the start date """
        return self.period[0]

    @property
    def end_date(self):
        """ End date of the selected period """
        return self.period[1]

    @property
    def period(self):
        """ Returns the period tuple """
        return datetimeutils.parse_period(self.period_str)


#@dataclass
class SchedTxRowViewModel: # pylint: disable=invalid-name
    """ result row for scheduled transactions """
    def __init__(self):
        self.name = None
        self.last_occurred = None
