"""
Displays the balance of a security across all accounts.
"""
import sys
from decimal import Decimal
from piecash import Commodity
from lib import database

def main(symbol):
    """
	Displays the balance for the security symbol.
	"""
    print("Displaying the balance for", symbol)
    db = database.Database()
    with db.open_book() as book:
        security = book.get(Commodity, mnemonic=symbol)
		#security.transactions, security.prices
        #total_balance = Decimal(0)
        total_quantity = Decimal(0)

        for account in security.accounts:
			# exclude Trading accouns explicitly.
            if account.type == "TRADING":
                continue

            balance = account.get_balance()
            quantity = account.get_quantity()

            print(account.fullname, balance, quantity)
			#total_balance += balance
            total_quantity += quantity

		#print("Balance:", total_balance)
        print("Quantity:", total_quantity)

#############################################################
# get the name of the security
symbol = None
print(AccountType)
if symbol:
	# When debugging, adjust the symbol manually.
    main(symbol)
else:
    if len(sys.argv) == 1:
        print("You need to provide the symbol for the security to be displayed.")
    else:
        symbol = sys.argv[1]
        main(symbol)
