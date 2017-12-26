""" Models for date/time operations """

from datetime import date, datetime


class DateRange:
    """ Range includes start and end dates """
    def __init__(self):
        self.start_date: date = None
        self.end_date: date = None

class DateTimeRange:
    """ Range includes start and end dates """
    def __init__(self):
        self.start_date: datetime = None
        self.end_date: datetime = None
