""" Tests for the Security Aggregate """
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securitiesaggregate import SecurityAggregate, SecuritiesAggregate


def test_account_type():
    """ Test account type import from piecash """
    with BookAggregate() as svc:
        securities = svc.securities.get_all()
        assert len(securities) > 0
        security = securities[0]
        sec_agg = svc.securities.get_aggregate(security)

        # This uses Account Type enum. If it doesn't break, everything is ok.
        avg_price = sec_agg.get_avg_price()

    assert avg_price


def test_income_last_12_mo():
    """ Test calculation of income in the last 12 months """
    from decimal import Decimal
    from pydatum import Datum

    with BookAggregate() as book:
        secs_agg = SecuritiesAggregate(book)
        sec = secs_agg.get_by_symbol("VSO")
        assert sec

        sec_agg = SecurityAggregate(book, sec)

        end = Datum()
        start = Datum()
        start.subtract_months(12)

        income = sec_agg.get_income_in_period(start, end)

    assert income
    assert income > Decimal(0)
