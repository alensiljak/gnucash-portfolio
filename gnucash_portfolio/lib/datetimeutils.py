""" Date/time utilities """

from datetime import datetime, date


def today_date() -> date:
    """ Returns today as a date """
    return datetime.today().date()

def get_from(period: str) -> datetime:
    """ Parse period string and return the from date """
    period_obj = parse_period(period)
    return period_obj[0]

def get_to(period: str) -> datetime:
    """ Parse period string and return the 'to' date """
    obj = parse_period(period)
    return obj[1]

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

def get_period(date_from: date, date_to: date) -> str:
    """ Returns the period string from the given dates """
    assert isinstance(date_from, date)
    assert isinstance(date_to, date)

    str_from: str = date_from.isoformat()
    str_to: str = date_to.isoformat()

    return str_from + " - " + str_to