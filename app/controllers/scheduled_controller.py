""" Scheduled Transactions """

#from logging import log, DEBUG
from typing import List
from flask import Blueprint, render_template, request
from piecash import ScheduledTransaction
from gnucash_portfolio.bookaggregate import BookAggregate
#from gnucash_portfolio.scheduledtxaggregate import ScheduledTxAggregate
from app.models.transaction_models import ScheduledTxInputModel


scheduled_controller = Blueprint( # pylint: disable=invalid-name
    'scheduled_controller', __name__, url_prefix='/scheduled')

@scheduled_controller.route('/', methods=['GET', 'POST'])
def scheduled_transactions():
    """ Lists scheduled transactions """
    input_model = __parse_sch_tx_search_params()

    if not input_model:
        # Initial run
        input_model = ScheduledTxInputModel()

    with BookAggregate() as svc:
        model = {
            "data": __load_model_for_scheduled_transactions(input_model, svc)
        }
        output = render_template('scheduled.html', model=model, input_model=input_model)
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
            "list": [tx for tx in upcoming]
        }
        return render_template('_scheduled.top10.html', model=model)

#################
# Private

def __parse_sch_tx_search_params() -> ScheduledTxInputModel:
    """ Parses the search parameters from the request """
    if not request.form:
        return None

    model = ScheduledTxInputModel()
    model.period_str = request.form.get("period")

    return model

def __load_model_for_scheduled_transactions(
        search: ScheduledTxInputModel, svc: BookAggregate) -> List[ScheduledTransaction]:
    """ loads data for scheduled transactions """
    if not search:
        return None

    query = svc.scheduled.get_all()
    return query
