"""
Displays the balance of a security across all accounts.
This logic is used in report_security_analysis.
"""
import sys
from decimal import Decimal
from piecash import Commodity
#from lib import database
import piecash

def main(symbol):
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

def get_avg_price(security):
    """
    Calculates the average price paid for the security.
    """
    avg_price = Decimal(0)

    #return sum([sp.quantity for sp in self.splits]) * self.sign

    for account in security.accounts:
        # Ignore trading accounts.
        if account.type == "TRADING":
            continue

        price_total = Decimal(0)
        price_count = 0

        for split in account.splits:
            price = split.value / split.quantity
            #print(price)
            price_count += 1
            price_total += price

    avg_price = price_total / price_count
    return avg_price

def get_number_of_shares(security):
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

#############################################################
# get the name of the security
#symbol = None
symbol = "VTIP"

if symbol:
	# When debugging, adjust the symbol manually.
    main(symbol)
else:
    if len(sys.argv) == 1:
        print("You need to provide the symbol for the security to be displayed.")
    else:
        symbol = sys.argv[1]
        main(symbol)
