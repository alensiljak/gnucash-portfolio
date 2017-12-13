"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
from flask import Blueprint, request, render_template
from piecash import Account
from sqlalchemy.ext.serializer import dumps
from gnucash_portfolio.lib.database import Database
import json

account_controller = Blueprint('account_controller', __name__, url_prefix='/account')


@account_controller.route('/')
def index():
    return render_template('incomplete.html')


@account_controller.route('/search')
def search():
    """ Search for an account by typing in a part of the name """
    return render_template('account.search.html')


@account_controller.route("/find")
def find():
    """ Search for an account with the given text in the name. Returns JSON result. """
    term = request.args.get("search[value]")
    model_array = []

    # Ignore empty requests
    if term:
        # Search in any part of the name
        term = '%' + term + '%'
        # search
        model_array = load_search_model(term)

    # data-table expected formatting. Unless I find a way to customize the client-side.
    model = {
        "data": model_array,
        "records_total": len(model_array)
    }
    json_output = json.dumps(model)
    return json_output

def load_search_model(search_term):
    """ Loads the data and returns an array of model objects"""
    model_array = []

    with Database().open_book() as book:
        records = (
            book.session.query(Account)
            .filter(Account.name.like(search_term))
            .all())

        for account in records:
            account_model = {
                "name": account.name,
                "fullname": account.fullname
            }
            model_array.append(account_model)

    return model_array
