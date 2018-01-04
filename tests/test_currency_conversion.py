""" Currency exchange rate conversion tests """

from gnucash_portfolio.bookaggregate import BookAggregate

def test_calculation_from_base_currency(svc_db: BookAggregate):
    """ Convert amount from base currency to destination currency """
    amount = 100
    source = "USD"
    destination = "EUR"

    actual = svc_db.currencies.get_amount_in_base_currency(source, amount)
    
    assert actual
