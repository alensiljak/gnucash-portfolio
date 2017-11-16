"""
Displays the balance of a security across all accounts.
"""
import sys
from piecash import Commodity
from lib import database

def main(symbol):
	"""
	Displays the balance for the security symbol.
	"""
	#print("ok, you thought this would be easy?")
	print("Displaying the balance for", symbol)
	db = database.Database()
	with db.open_book() as book:
		security = book.get(Commodity, mnemonic=symbol)
		#print(security.transactions)
		# security.prices
		total = 0
		for account in security.accounts:
			balance = account.get_balance()
			print(account.fullname, balance)
			total += balance
		
		print(total)

#############################################################
# get the name of the security
symbol = None

if symbol:
	# When debugging, adjust the symbol manually.
	main(symbol)
else:
	if len(sys.argv) == 1:
		print("You need to provide the symbol for the security to be displayed.")
	else:
		symbol = sys.argv[1]
		main(symbol)
