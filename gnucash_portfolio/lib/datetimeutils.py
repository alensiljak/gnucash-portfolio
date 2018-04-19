""" Date/time utilities """
import calendar
from datetime import date, datetime

from pydatum import Datum


def get_days_in_month(year: int, month: int) -> int:
    """ Returns number of days in the given month.
    1-based numbers as arguments. i.e. November = 11 """
    month_range = calendar.monthrange(year, month)
    return month_range[1]


def get_from_gnucash26_date(date_str: str) -> date:
    """ Creates a datetime from GnuCash 2.6 date string """
    date_format = "%Y%m%d"
    result = datetime.strptime(date_str, date_format).date()
    return result


def get_period_start(period: str) -> datetime:
    """ Parse period string and return the from date """
    period_obj = parse_period(period)
    return period_obj[0]


def get_period_end(period: str) -> datetime:
    """ Parse period string and return the 'to' date """
    obj = parse_period(period)
    return obj[1]


def parse_period(period: str):
    """ parses period from date range picker. The received values are full ISO date """
    period = period.split(" - ")

    date_from = Datum()
    if len(period[0]) == 10:
        date_from.from_iso_date_string(period[0])
    else:
        date_from.from_iso_long_date(period[0])
    date_from.start_of_day()

    date_to = Datum()
    if len(period[1]) == 10:
        date_to.from_iso_date_string(period[1])
    else:
        date_to.from_iso_long_date(period[1])
    date_to.end_of_day()

    return date_from.value, date_to.value


def parse_us_date(date_us: str) -> datetime:
    """ Parses US date mm/dd/yyyy """
    return datetime.strptime(date_us, "%m/%d/%Y")


def get_period(date_from: date, date_to: date) -> str:
    """ Returns the period string from the given dates """
    assert isinstance(date_from, date)
    assert isinstance(date_to, date)

    str_from: str = date_from.isoformat()
    str_to: str = date_to.isoformat()

    return str_from + " - " + str_to


def get_period_last_week() -> str:
    """ Returns the last week as a period string """
    today = Datum()
    today.start_of_day()
    # start_date = today - timedelta(days=7)
    start_date = today.clone()
    start_date.subtract_days(7)

    period = get_period(start_date.value, today.value)
    return period


def get_period_last_30_days() -> str:
    """ Returns the last week as a period string """
    today = Datum()
    today.today()
    # start_date = today - timedelta(days=30)
    start_date = today.clone()
    start_date.subtract_days(30)

    period = get_period(start_date.value, today.value)
    return period


def get_period_last_3_months() -> str:
    """ Returns the last week as a period string """
    today = Datum()
    today.today()

    # start_date = today - timedelta(weeks=13)
    start_date = today.clone()
    start_date.subtract_months(3)

    period = get_period(start_date.date, today.date)
    return period
