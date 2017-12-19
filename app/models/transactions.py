""" Models for Transactions """

class ScheduledTxSearchModel:
    """ Input model for scheduled transactions list """
    def __init__(self):
        self.date_from = None
        self.date_to = None


class SchedTxRowViewModel:
    """ result row for scheduled transactions """
    def __init__(self):
        self.name = None
        self.start_date = None
        self.last_occurred = None
