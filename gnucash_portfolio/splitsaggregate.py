'''
Splits.
Currently not needed as the splits can be filtered through transaction
and account aggregates.
'''
from typing import List
from piecash import Book, Split, Account


class SplitAggregate:
    def __init__(self, split: Split, book: Book):
        self.split = split
        self.book = book

class SplitsAggregate:
    ''' split collections '''
    def __init__(self, book: Book):
        self.book = book

    @property
    def query(self):
        query = (
            self.book.session.query(Split)
        )
        return query

    def get(self, split_id: str) -> Split:
        """ load transaction by id """
        query = (
            self.query
            .filter(Split.guid == split_id)
        )
        return query.one()

    def get_aggregate(self, split: Split) -> SplitAggregate:
        """ Returns the transaction aggregate for transaction """
        return SplitAggregate(split, self.book)

    def get_for_accounts(self, accounts: List[Account]):
        ''' Get all splits for the given accounts '''
        account_ids = [acc.guid for acc in accounts]
        query = (
            self.query
            .filter(Split.account_guid.in_(account_ids))
        )
        splits = query.all()
        return splits
