""" Tests for Scheduled Accounts Aggregate """

from logging import log, DEBUG
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib import datetimeutils


def test_get_all(svc_db: BookAggregate):
    """ Get all scheduled transaction records """
    txs = svc_db.scheduled.get_all()

    assert len(txs) == 1

def test_next_date(svc_db: BookAggregate):
    """ Check the next date for the transaction """
    tx_id = '085ce0d6e2dfccd36c8db442afafad9f'
    expected = datetimeutils.get_from_gnucash26_date("20171230")

    tx = svc_db.scheduled.get_by_id(tx_id)

    assert tx.start_date == expected

def test_get_upcoming(svc_db: BookAggregate):
    """ Test the upcoming transactions list """
    actual = svc_db.scheduled.get_upcoming(10)

    for tx in actual:
        log(DEBUG, tx["next_date"])

    assert len(actual) == 10
