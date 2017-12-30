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
    # No hours in date.
    # assert actual.hour == 0

def test_parsing_iso_date():
    """ Parse ISO date """
    value = "2017-12-31"

    actual = datetimeutils.parse_iso_date(value)

    assert actual
    assert actual.year == 2017
    assert actual.month == 12
    assert actual.day == 31
