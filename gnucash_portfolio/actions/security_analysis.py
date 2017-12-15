"""
Various operations on commodities / securities / stocks.

Displays the balance of a security across all accounts.
This logic is used in report_security_analysis.
"""
import sys
from decimal import Decimal
from piecash import Commodity, Book, Price
from gnucash_portfolio.lib import database
from gnucash_portfolio.securityaggregate import SecurityAggregate

def main(symbol: str):
    """
	Displays the balance for the security symbol.
	"""
    print("Displaying the balance for", symbol)
    db = database.Database()
    with db.open_book() as book:
        security = book.get(Commodity, mnemonic=symbol)
		#security.transactions, security.prices

        svc = SecurityAggregate(book)

        # Display number of shares
        shares_no = svc.get_number_of_shares(security)
        print("Quantity:", shares_no)

        # Calculate average price.
        avg_price = svc.get_avg_price(security)
        print("Average price:", avg_price)
