""" Scheduled Transactions """

from piecash import Book, ScheduledTransaction, Recurrence


class ScheduledTxAggregate:
    """ Handles single scheduled transaction entity """

    def __init__(self, book: Book, tx: ScheduledTransaction):
        self.book = book
        self.transaction = tx


class ScheduledTxsAggregate:
    """ Agregate for collection """
    def __init__(self, book: Book):
        self.book = book

    def get_upcoming(self, count: int):
        """ Returns <count> upcoming scheduled transactions """
        # load all transactions
        all_tx = self.get_all()
        # TODO calculate next occurrence date
        for tx in all_tx:
            self.__calculate_next_occurrence(tx)
        # TODO order by next occurrence date
        #tx.sort()
        # TODO get upcoming (top) 10
        return all_tx

    def get_all(self):
        """ All scheduled transactions """
        return self.query.all()

    def get_by_id(self, tx_id: str) -> ScheduledTransaction:
        """ Fetches a tx by id """
        return self.query.filter(ScheduledTransaction.guid == tx_id).first()

    def get_aggregate_for(self, tx: ScheduledTransaction) -> ScheduledTxAggregate:
        """ Creates an aggregate for single entity """
        return ScheduledTxAggregate(self.book, tx)

    @property
    def query(self):
        """ The main query """
        query = (
            self.book.session.query(ScheduledTransaction)
        )
        return query

    ##################
    # Private

    def __get_ordered_list(self):
        """ retrieves ordered list of Scheduled Transactions """
        pass

    def __calculate_next_occurrence(self, tx: ScheduledTransaction):
        """ Calculates the next occurrence date for scheduled transaction """
        base_date = tx.last_occur if tx.last_occur else tx.start_date
        print(base_date)
        print(tx.recurrence.recurrence_period_start)
        print(tx.recurrence.recurrence_mult)
        print(tx.recurrence.recurrence_period_type)

        # TODO check the datetime libraries for scheduler

        tx["next_date"] = base_date
