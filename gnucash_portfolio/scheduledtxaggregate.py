""" Scheduled Transactions """

from typing import List
from enum import Enum
from logging import log, DEBUG, INFO, WARN
from datetime import date, datetime
from piecash import Book, ScheduledTransaction #, Recurrence
from gnucash_portfolio.lib import datetimeutils


class RecurrencePeriod(Enum):
    """ Recurrence Types """
    #ROOT = auto()
    YEAR = "year"
    MONTH = "month"
    END_OF_MONTH = "end of month"
    DAY = "day"


def get_next_occurrence(tx: ScheduledTransaction) -> date:
    """ Calculates the next occurrence date for scheduled transaction.
    Mimics the recurrenceNextInstance() function from GnuCash.
    Still not complete but handles the main cases I use. """
    # Reference documentation:
    # https://github.com/MisterY/gnucash-portfolio/issues/3

    # Preparing ref day is an important part before the calculation.
    ref_date: datetime = None
    # It should be: a) the last occurrence date; or b) the recurrence start date.
    if tx.last_occur:
        ref_date = tx.last_occur
    if not ref_date:
        ref_date = tx.recurrence.recurrence_period_start
    today = datetimeutils.today_date()
    if ref_date > today:
        ref_date = today

    ###########################################################
    # The code below mimics the function
    # recurrenceNextInstance(const Recurrence *r, const GDate *refDate, GDate *nextDate)

    start_date: datetime = tx.recurrence.recurrence_period_start
    if ref_date < start_date:
        # If the occurrence hasn't even started, the next date is the start date.
        # this should also handle the "once" type in most cases.
        return start_date

    # start at refDate.
    next_date: datetime = ref_date

    # last_date: datetime = tx.last_occur
    # print(tx.name, base_date, tx.recurrence.recurrence_period_start,
    #       tx.recurrence.recurrence_mult, tx.recurrence.recurrence_period_type)

    # /* Step 1: move FORWARD one period, passing exactly one occurrence. */

    mult: int = tx.recurrence.recurrence_mult
    period: str = tx.recurrence.recurrence_period_type
    #wadj = tx.recurrence.recurrence_weekend_adjust

    if period in ([RecurrencePeriod.YEAR.value, RecurrencePeriod.MONTH.value,
                   RecurrencePeriod.END_OF_MONTH.value]):
        if period == RecurrencePeriod.YEAR.value:
            mult *= 12

        # handle weekend adjustment here.

        # Line 274.
        if (datetimeutils.is_end_of_month(next_date) or
                (period in [RecurrencePeriod.MONTH.value, RecurrencePeriod.YEAR.value]
                 and (next_date.day >= start_date.day))
           ):
            next_date = datetimeutils.add_months(next_date, mult)
            # Set at end of month again (?!)
            #next_date = datetimeutils.get_end_of_month(next_date)
        else:
            next_date = datetimeutils.add_months(next_date, mult - 1)

    # elif period == "once":
    #     next_date = tx.recurrence.recurrence_period_start

    elif period == RecurrencePeriod.DAY.value:
        log(WARN, "daily not handled")

    else:
        log(INFO, "recurrence not handled: %s", period)

    #######################
    # Step 2

    if period in ([RecurrencePeriod.YEAR.value, RecurrencePeriod.MONTH.value,
                   RecurrencePeriod.END_OF_MONTH.value]):
        n_months = (
            12 * (next_date.year - start_date.year) +
            (next_date.month - start_date.month)
        )
        next_date = datetimeutils.subtract_months(next_date, n_months % mult)

        # dim
        days_in_month = datetimeutils.get_days_in_month(next_date.year, next_date.month)

        # Handle adjustment for 3 ways.
        if (period == RecurrencePeriod.END_OF_MONTH.value or
                next_date.day >= days_in_month):
            # Set to last day of the month.
            next_date = next_date.replace(day=days_in_month)
        else:
            # Same day as the start.
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

    def get_all(self) -> List[ScheduledTransaction]:
        """ All scheduled transactions """
        return self.query.all()

    def get_enabled(self) -> List[ScheduledTransaction]:
        """ Returns only enabled scheduled transactions """
        query = (
            self.query
            .filter(ScheduledTransaction.enabled == True)
        )
        return query.all()

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
