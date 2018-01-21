""" Transactions aggregate """

from decimal import Decimal
from piecash import Book, Transaction, Split

class TransactionAggregate:
    """ Single-item aggregate """
    def __init__(self, tx: Transaction, book: Book):
        self.book = book
        self.transaction = tx

    def get_splits_query(self):
        """ Returns the query for related splits """
        query = (
            self.book.session.query(Split)
            # .join(Transaction)
            .filter(Split.transaction_guid == self.transaction.guid)
        )
        return query

    def get_split_for_account(self, account_id: str) -> Split:
        query = (
            self.get_splits_query()
            # .join(Account)
            .filter(Split.account_guid == account_id)
        )
        return query.all()

    def get_value_of_splits_for_account(self, account_id: str) -> Decimal:
        """ Returns the sum of values for all splits for the given account """
        splits = self.get_split_for_account(account_id)
        result = Decimal(0)
        for split in splits:
            result += split.value
        return result

    def get_quantity_of_splits_for_account(self, account_id: str) -> Decimal:
        """ Returns the sum of values for all splits for the given account """
        splits = self.get_split_for_account(account_id)
        result = Decimal(0)
        for split in splits:
            result += split.quantity
        return result


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

    def get_aggregate(self, tx: Transaction) -> TransactionAggregate:
        """ Returns the transaction aggregate for transaction """
        return TransactionAggregate(tx, self.book)
