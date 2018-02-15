""" Tests for the Security Aggregate """
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate

def test_account_type():
    """ Test account type import from piecash """
    with BookAggregate() as svc:
        securities = svc.securities.get_all()
        assert len(securities) > 0
        security = securities[0]
        sec_agg = svc.securities.get_aggregate(security)

        # This uses Account Type enum. If it doesn't break, everything is ok.
        avg_price = sec_agg.get_avg_price()

