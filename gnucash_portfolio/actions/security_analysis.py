"""
Various operations on commodities / securities / stocks.

Displays the balance of a security across all accounts.
This logic is used in report_security_analysis.
"""
import sys
from decimal import Decimal
from piecash import Commodity, Book, Price
from gnucash_portfolio.lib import database
from gnucash_portfolio.securityaggregate import StockAggregate

def main(symbol: str):
    """
	Displays the balance for the security symbol.
	"""
    print("Displaying the balance for", symbol)
    db = database.Database()
    with db.open_book() as book:
        security = book.get(Commodity, mnemonic=symbol)
		#security.transactions, security.prices

        # Display number of shares
        svc = StockAggregate(book)
        shares_no = svc.get_number_of_shares(security)
        print("Quantity:", shares_no)

        # Calculate average price.
        avg_price = get_avg_price(security)
        print("Average price:", avg_price)


def get_avg_price(security: Commodity) -> Decimal:
    """
    Calculates the average price paid for the security.
    security = Commodity
    Returns Decimal value.
    """
    #print("Calculating stats for", security.mnemonic)
    avg_price = Decimal(0)

    #return sum([sp.quantity for sp in self.splits]) * self.sign

    price_total = Decimal(0)
    price_count = 0

    for account in security.accounts:
        # Ignore trading accounts.
        if account.type == "TRADING":
            continue

        for split in account.splits:
            # Don't count the non-transactions.
            if split.quantity == 0:
                continue

            price = split.value / split.quantity
            #print(price)
            price_count += 1
            price_total += price

    #print(price_total, price_count)
    if price_count:
        avg_price = price_total / price_count
    return avg_price


#####################################################################
# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         print("You need to provide the symbol for the security to be displayed.")
#         # Show the demo.
#         demo()
#     else:
#         symbol = sys.argv[1]
#         main(symbol)
