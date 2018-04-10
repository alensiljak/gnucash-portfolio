""" Scheduled Transactions """

from datetime import date
from typing import List

from flask import Blueprint, render_template, request

from app.models.transaction_models import ScheduledTxInputModel
from gnucash_portfolio.bookaggregate import BookAggregate
from piecash import ScheduledTransaction

try:
    import simplejson as json
except ImportError:
    import json


scheduled_controller = Blueprint(  # pylint: disable=invalid-name
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
        output = render_template(
            'scheduled.html', model=model, input_model=input_model)
    return output


@scheduled_controller.route('/calendar')
def calendar():
    """ Full Calendar """
    # todo load data
    return render_template('scheduled.calendar.html')


@scheduled_controller.route('/duedate')
def scheduled_with_due_date():
    """ Returns scheduled transactions with their next occurrence date """
    input_model = __parse_sch_tx_search_params()
    if not input_model:
        # Initial run
        input_model = ScheduledTxInputModel()

    with BookAggregate() as svc:
        transactions = __load_model_for_scheduled_transactions(
            input_model, svc)
        transactions = __load_due_dates(svc, transactions)
        model = {
            "data": transactions
        }
        output = render_template(
            'scheduled.duedate.html', model=model, input_model=input_model)
    return output

##################
# API


@scheduled_controller.route('/api/top10')
def api_top_10():
    return api_transactions(10)


@scheduled_controller.route('/api/transactions/<int:count>')
def api_transactions(count: int):
    """ Returns next n scheduled transactions in JSON """
    assert isinstance(count, int)

    with BookAggregate() as svc:
        upcoming = svc.scheduled.get_upcoming(count)
        result = __get_api_model_from_sx(upcoming)
        json_result = json.dumps(result)
    return json_result

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


def __get_api_model_from_sx(transactions: List[ScheduledTransaction]):
    from pydatum import Datum

    result = []
    for tx in transactions:
        start_date = Datum()
        start_date.from_date(tx["next_date"].value)

        result.append({
            "title": tx.name,
            "start": start_date.get_iso_string(),
            "allDay": True
        })
    return result

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

    query = svc.scheduled.get_enabled()
    return query

def __load_due_dates(
        svc: BookAggregate, transactions: List[ScheduledTransaction]
) -> List[ScheduledTransaction]:
    """ Populates due dates on scheduled transactions """
    for sx in transactions:
        agg = svc.scheduled.get_aggregate_for(sx)
        next_occurrence = agg.get_next_occurrence()
        assert isinstance(next_occurrence, date)
        sx["due_date"] = next_occurrence

    return transactions
