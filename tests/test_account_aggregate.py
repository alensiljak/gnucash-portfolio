""" Tests for Accounts Aggregate """

from logging import log, DEBUG
from gnucash_portfolio.bookaggregate import BookAggregate


def test_get_by_fullname(svc_db: BookAggregate):
    log(DEBUG, "using book %s", svc_db.book)

    name = "Assets:Investment"
    assert name == ""
