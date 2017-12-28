""" Date/time utilities """

from datetime import datetime, date, time, timedelta
#import calendar

def get_from_gnucash26_date(date_str: str) -> datetime:
    """ Creates a datetime from GnuCash 2.6 date string """
    date_format = "%Y%m%d"
    result = datetime.strptime(date_str, date_format)
    return result

def today_date() -> date:
    """ Returns today as a date """
    return datetime.today().date()

def today_datetime() -> datetime:
    """ Returns today (date only) as datetime """
    date_today = today_date()
    today = datetime.combine(date_today, time.min)
    return today

def get_period_start(period: str) -> datetime:
    """ Parse period string and return the from date """
    period_obj = parse_period(period)
    return period_obj[0]

def get_period_end(period: str) -> datetime:
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

def get_period_last_week() -> str:
    """ Returns the last week as a period string """
    today = today_date()
    start_date = today - timedelta(days=7)
    period = get_period(start_date, today)
    return period

def get_period_last_3_months() -> str:
    """ Returns the last week as a period string """
    today = today_date()
    start_date = today - timedelta(weeks=13)
    period = get_period(start_date, today)
    return period
