""" Tests for Accounts Aggregate """

from logging import log, DEBUG
from gnucash_portfolio.bookaggregate import BookAggregate


def test_get_by_fullname(svc_db: BookAggregate):
    log(DEBUG, "using book %s", svc_db.book)
    name = "Assets:Investments"

    acct = svc_db.accounts.get_account_by_fullname(name)

    assert acct.fullname == name


def test_get_all_children(svc_db: BookAggregate):
    name = "Assets:Investments"

    children = svc_db.accounts.get_all_children(name)

    assert children
