"""
Transactions & Splits
- account register with search (by description & memo) & filtering (date), sorting
- editing of transaction splits
- display transaction details with splits
"""
from typing import List
from flask import Blueprint, request, render_template
from piecash import Book, ScheduledTransaction
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.scheduledtxaggregate import ScheduledTxAggregate
from gnucash_portfolio.transactionaggregate import TransactionsAggregate
from models.transactions import ScheduledTxSearchModel

transaction_controller = Blueprint('transaction_controller', __name__, url_prefix='/transaction')

@transaction_controller.route('/details/<tx_id>')
def tx_details(tx_id: str):
    """ Display transaction details """
    with BookAggregate() as svc:
        tx_svc = TransactionsAggregate(svc.book)
        tx = tx_svc.get(tx_id)
        #print(tx.description)
        model = {
            "transaction": tx
        }
        return render_template('transaction.details.html', model=model)


@transaction_controller.route('/scheduled', methods=['GET', 'POST'])
def scheduled_transactions():
    """ Lists scheduled transactions """
    search_model = __parse_sch_tx_search_params(request)
    if not search_model:
        # Initial run
        search_model = ScheduledTxSearchModel()

    with BookAggregate() as svc:
        model = {
            "search": None,
            "data": __load_model_for_scheduled_transactions(search_model, svc.book)
        }
        output = render_template('transaction.scheduled.html', model=model)
    return output


def __parse_sch_tx_search_params(request) -> ScheduledTxSearchModel:
    """ Parses the search parameters from the request """
    if not request.form:
        return None

    search_model = ScheduledTxSearchModel()
    return search_model


def __load_model_for_scheduled_transactions(
        search: ScheduledTxSearchModel, book: Book) -> List[ScheduledTransaction]:
    """ loads data for scheduled transactions """
    if not search:
        return None

    svc = ScheduledTxAggregate(book)
    query = svc.get_all_query()
    return query.all()
