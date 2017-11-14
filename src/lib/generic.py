"""
Generic utilities
"""
import time
from datetime import datetime, timedelta

def get_today():
    """
    Returns the current date string in ISO format.
    """
    return get_date_iso_string(time)

def get_yesterday():
    """
    Returns yesterday's datetime
    """
    return datetime.today() - timedelta(days=1)

def get_date_iso_string(value):
    return value.strftime("%Y-%m-%d")
