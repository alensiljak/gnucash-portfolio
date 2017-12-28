""" Tests for datetime utilities """

from logging import log, DEBUG
from gnucash_portfolio.lib import datetimeutils


def test_parsing_gc26_date():
    """ Parse GnuCash 2.6 date format """
    value = "20171230"

    actual = datetimeutils.get_from_gnucash26_date(value)
    log(DEBUG, actual)

    assert actual.year == 2017
    assert actual.month == 12
    assert actual.day == 30
    assert actual.hour == 0
