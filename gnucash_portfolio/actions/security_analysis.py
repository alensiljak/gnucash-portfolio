"""
Various operations on commodities / securities / stocks.

Displays the balance of a security across all accounts.
This logic is used in report_security_analysis.
"""
from piecash import Commodity
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securities import SecurityAggregate


def main(symbol: str):
    """
	Displays the balance for the security symbol.
	"""
    print("Displaying the balance for", symbol)

    with BookAggregate() as svc:
        security = svc.book.get(Commodity, mnemonic=symbol)
		#security.transactions, security.prices

        sec_svc = SecurityAggregate(svc.book, security)

        # Display number of shares
        shares_no = sec_svc.get_quantity()
        print("Quantity:", shares_no)

        # Calculate average price.
        avg_price = sec_svc.get_avg_price()
        print("Average price:", avg_price)
