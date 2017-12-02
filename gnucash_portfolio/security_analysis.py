"""
Various operations on commodities / securities / stocks.

Displays the balance of a security across all accounts.
This logic is used in report_security_analysis.
"""
import sys
from decimal import Decimal
from sqlalchemy import desc
from piecash import Commodity, Book, Price
from gnucash_portfolio.lib import database

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
        shares_no = get_number_of_shares(security)
        print("Quantity:", shares_no)

        # TODO Calculate average price.
        avg_price = get_avg_price(security)
        print("Average price:", avg_price)

def get_stock(book: Book, symbol: str) -> Commodity:
    """Returns the stock/commodity object for the given symbol"""
    #with database.Database().open_book() as book:
    security = book.get(Commodity, mnemonic=symbol)

    return security

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

def get_number_of_shares(security: Commodity) -> Decimal:
    """
    Returns the number of shares for the given security.
    It gets the number from all the accounts in the book.
    """
    total_quantity = Decimal(0)
    #total_balance = Decimal(0)

    for account in security.accounts:
        # exclude Trading accouns explicitly.
        if account.type == "TRADING":
            continue

        balance = account.get_balance()
        quantity = account.get_quantity()

        #print(account.fullname, quantity, balance)
        #total_balance += balance
        total_quantity += quantity

    #print("Balance:", total_balance)
    return total_quantity

def get_last_available_price(security: Commodity) -> Decimal:
    """Finds the last available price for commodity"""
    last_price = security.prices.order_by(desc(Price.date)).first()
    return last_price.value

def demo():
    # generate a dummy security
    sec = Commodity(namespace="ASX", mnemonic="VHY", fullname="Vanguard High Yield ETF")
    # TODO add transactions.

    # display output

    num_shares = get_number_of_shares(sec)
    print("Number of shares", num_shares)

    avg_price = get_avg_price(sec)
    print("Average price", avg_price)

#####################################################################
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You need to provide the symbol for the security to be displayed.")
        # Show the demo.
        demo()
    else:
        symbol = sys.argv[1]
        main(symbol)
