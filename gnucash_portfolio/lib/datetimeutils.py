""" Date/time utilities """

from datetime import datetime


def parse_period(period: str):
    """ parses period from date range picker """
    period = period.split(" - ")
    date_from = datetime.strptime(period[0], "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    date_to = datetime.strptime(period[1], "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    return (date_from, date_to)

def start_of_day(datum: datetime) -> datetime:
    """ Returns start of day """
    return datetime(datum.year, datum.month, datum.day)

def end_of_day(datum: datetime) -> datetime:
    """ End of day """
    return datetime(datum.year, datum.month, datum.day, 23, 59, 59)