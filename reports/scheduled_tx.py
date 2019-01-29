"""
Show scheduled transactions
"""
from gnucash_portfolio import BookAggregate

book = BookAggregate()
txs = book.scheduled.get_upcoming(10)
for tx in txs:
    print(tx)
