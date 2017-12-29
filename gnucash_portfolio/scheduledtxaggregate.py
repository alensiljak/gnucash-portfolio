""" Scheduled Transactions """

from typing import List
from logging import log, DEBUG, INFO, WARN
from datetime import date
from piecash import Book, ScheduledTransaction #, Recurrence
from gnucash_portfolio.lib import datetimeutils


def get_next_occurrence(tx: ScheduledTransaction) -> date:
    """ Calculates the next occurrence date for scheduled transaction """
    # Reference documentation:
    # https://github.com/MisterY/gnucash-portfolio/issues/3

    ref_date = datetimeutils.today_date()
    start_date = tx.recurrence.recurrence_period_start
    last_date = tx.last_occur

    if start_date > ref_date:
        # If the occurrence hasn't even started, the next date is the start date.
        # this should also handle the "once" type in most cases.
        return start_date

    if not last_date:
        last_date = start_date

    # print(tx.name, base_date, tx.recurrence.recurrence_period_start,
    #       tx.recurrence.recurrence_mult, tx.recurrence.recurrence_period_type)
    next_date = last_date
    period = tx.recurrence.recurrence_period_type
    mult = tx.recurrence.recurrence_mult
    #wadj = tx.recurrence.recurrence_weekend_adjust

    if period == "day":
        log(WARN, "daily not handled")

    elif period in ["year", "month", "end of month"]:
        if period == "year":
            mult *= 12

        # handle weekend adjustment

        # if the date is already at end of month, then increase
        if datetimeutils.is_end_of_month(next_date):
            next_date = datetimeutils.add_months(next_date, mult)
            # Set at end of month again
            next_date = datetimeutils.get_end_of_month(next_date)
        else:
            next_date = datetimeutils.add_months(next_date, mult - 1)

    # elif period == "once":
    #     next_date = tx.recurrence.recurrence_period_start
    else:
        log(INFO, "recurrence not handled: %s", period)

    #######################
    # Step 2

    if period in ["year", "month", "end of month"]:
        n_months = (
            12 * (next_date.year - start_date.year) +
            (next_date.month - start_date.month)
        )
        next_date = datetimeutils.subtract_months(next_date, n_months % mult)
        # Handle adjustment for 3 ways.
        # Here we take only the simple, last one.
        next_date = next_date.replace(day=start_date.day)

        # handle weekend

    return next_date


class ScheduledTxAggregate:
    """ Handles single scheduled transaction entity """

    def __init__(self, book: Book, tx: ScheduledTransaction):
        self.book = book
        self.transaction = tx

    def get_next_occurrence(self) -> date:
        """ Returns the next occurrence date for transaction """
        return get_next_occurrence(self.transaction)


class ScheduledTxsAggregate:
    """ Agregate for collection """
    def __init__(self, book: Book):
        self.book = book

    def get_upcoming(self, count: int) -> List[ScheduledTransaction]:
        """ Returns <count> upcoming scheduled transactions """
        # load all enabled scheduled transactions
        all_tx = self.query.filter(ScheduledTransaction.enabled == 1).all()

        # calculate next occurrence date
        for tx in all_tx:
            next_date = get_next_occurrence(tx)
            tx["next_date"] = next_date

        # order by next occurrence date
        all_tx.sort(key=lambda tx: tx["next_date"].value)
        # get upcoming (top) 10
        top_n = all_tx[:count]
        return top_n

    def get_all(self):
        """ All scheduled transactions """
        return self.query.all()

    def get_by_id(self, tx_id: str) -> ScheduledTransaction:
        """ Fetches a tx by id """
        return self.query.filter(ScheduledTransaction.guid == tx_id).first()

    def get_aggregate_for(self, tx: ScheduledTransaction) -> ScheduledTxAggregate:
        """ Creates an aggregate for single entity """
        return ScheduledTxAggregate(self.book, tx)

    def get_aggregate_by_id(self, tx_id: str) -> ScheduledTxAggregate:
        """ Creates an aggregate for single entity """
        tran = self.get_by_id(tx_id)
        return self.get_aggregate_for(tran)

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
