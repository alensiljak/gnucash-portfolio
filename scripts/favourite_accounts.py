"""
    Display favourite accounts with balances.
    The accounts are stored in GC Portfolio config file (gnucash_portfolio.json)
"""

# get the list of accounts
from gnucash_portfolio import BookAggregate
from piecash import Account

book = BookAggregate()
fav_unsorted = book.accounts.get_favourite_accounts()
favorites = sorted(fav_unsorted, key=lambda account: account.name)

x: Account = None

# Output
for account in favorites:
    balance = account.get_balance()
    print(f"{account.name:<25}{balance:>10,}")
