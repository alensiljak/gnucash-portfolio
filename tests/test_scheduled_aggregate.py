""" Tests for Scheduled Accounts Aggregate """

from logging import log, DEBUG
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib import datetimeutils


def test_get_all(svc_db: BookAggregate):
    """ Get all scheduled transaction records """
    txs = svc_db.scheduled.get_all()

    assert len(txs) == 2

def test_start_date(svc_db: BookAggregate):
    """ Check the next date for the transaction """
    tx_id = '085ce0d6e2dfccd36c8db442afafad9f'
    expected = datetimeutils.get_from_gnucash26_date("20171213")

    tx = svc_db.scheduled.get_by_id(tx_id)

    assert tx.start_date == expected

def test_next_date_field(svc_db: BookAggregate):
    """ Test calculation of the next date for 1 transaction """
    tx_id = '085ce0d6e2dfccd36c8db442afafad9f' # Monthly Tx
    expected = datetimeutils.get_from_gnucash26_date("20171214")

    tx = svc_db.scheduled.get_aggregate_by_id(tx_id)
    actual = tx.get_next_occurrence()

    assert actual == expected
    assert tx.transaction.enabled == 1

# This is now quarterly schedule.
# def test_weekly_calculation(svc_db: BookAggregate):
#     """ Test calculation of weekly schedule """
#     tx_id = '959661fa0e0487ec2933a53960584963'
#     expected = datetimeutils.get_from_gnucash26_date("20171205")

#     tx = svc_db.scheduled.get_aggregate_by_id(tx_id)
#     actual = tx.get_next_occurrence()

#     assert actual == expected

def test_monthly_calculation(svc_db: BookAggregate):
    """ Test calculation of monthly recurrence """
    tx_id = '085ce0d6e2dfccd36c8db442afafad9f' # Monthly Tx
    expected = datetimeutils.get_from_gnucash26_date("20171214")

    tx = svc_db.scheduled.get_aggregate_by_id(tx_id)
    actual = tx.get_next_occurrence()

    assert actual == expected

def test_get_upcoming(svc_db: BookAggregate):
    """ Test the upcoming transactions list """
    actual = svc_db.scheduled.get_upcoming(10)

    for tx in actual:
        # All returned records must be enabled
        assert tx.enabled == True

    assert len(actual) == 2
