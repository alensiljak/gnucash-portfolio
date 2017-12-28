""" Scheduled Transactions """

from typing import List
from flask import Blueprint, render_template, request
from piecash import ScheduledTransaction
from gnucash_portfolio.bookaggregate import BookAggregate
#from gnucash_portfolio.scheduledtxaggregate import ScheduledTxAggregate
from app.models.transaction_models import ScheduledTxSearchModel

scheduled_controller = Blueprint( # pylint: disable=invalid-name
    'scheduled_controller', __name__, url_prefix='/scheduled')

@scheduled_controller.route('/scheduled', methods=['GET', 'POST'])
def scheduled_transactions():
    """ Lists scheduled transactions """
    search_model = __parse_sch_tx_search_params()
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

##################
# Partials

@scheduled_controller.route('/partial/top10')
def topten_partial():
    """ Partial for scheduled transactions. Displays ten upcoming transactions
    for the dashboard. """
    with BookAggregate() as svc:
        upcoming = svc.scheduled.get_upcoming(10)
        model = {
            "list": [{"key": tx.guid, "value": tx.name} for tx in upcoming]
        }
        return render_template('_scheduled.top10.html', model=model)

#################
# Private

def __parse_sch_tx_search_params() -> ScheduledTxSearchModel:
    """ Parses the search parameters from the request """
    if not request.form:
        return None

    search_model = ScheduledTxSearchModel()
    return search_model

def __load_model_for_scheduled_transactions(
        search: ScheduledTxSearchModel, svc: BookAggregate) -> List[ScheduledTransaction]:
    """ loads data for scheduled transactions """
    if not search:
        return None

    query = svc.scheduled.get_all()
    return query
