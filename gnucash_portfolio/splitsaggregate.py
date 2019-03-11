'''
Splits.
Currently not needed as the splits can be filtered through transaction
and account aggregates.
'''
from decimal import Decimal
from piecash import Book, Split

# class SplitAggregate:
#     def __init__(self, book: Book):
#         self.book = book

# class SplitsAggregate:
#     ''' split collections '''
#     def __init__(self, book: Book):
#         self.book = book

#     def get(self, tx_id: str) -> Transaction:
#         """ load transaction by id """
#         query = (
#             self.book.session.query(Transaction)
#             .filter(Transaction.guid == tx_id)
#         )
#         return query.one()

#     def get_aggregate(self, tx: Transaction) -> TransactionAggregate:
#         """ Returns the transaction aggregate for transaction """
#         return TransactionAggregate(tx, self.book)
