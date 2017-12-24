""" Transactions aggregate """

from piecash import Book, Transaction


class TransactionsAggregate:
    """ transaction collections """
    def __init__(self, book: Book):
        self.book = book

    def get(self, tx_id: str) -> Transaction:
        """ load transaction by id """
        query = (
            self.book.session.query(Transaction)
            .filter(Transaction.guid == tx_id)
        )
        return query.one()
