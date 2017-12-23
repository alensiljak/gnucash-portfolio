""" Scheduled Transactions """

from piecash import Book, ScheduledTransaction


class ScheduledTxAggregate:
    """ Handles scheduled transactions
    Look for gsltma_get_sx_instances_from_orig_iter in GnuCash.
    """

    def __init__(self, book: Book):
        self.book = book

    def get_all_query(self):
        """ returns the query with all scheduled transactions """
        query = (
            self.book.session.query(ScheduledTransaction)
        )
        return query

    def get_all(self):
        """ returns all scheduled transactions """
        return self.get_all_query().all()
