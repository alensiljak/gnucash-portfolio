"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
import json
from flask import Blueprint, request, render_template
from piecash import Account
#from sqlalchemy.ext.serializer import dumps
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate


account_controller = Blueprint('account_controller', __name__, url_prefix='/account')


@account_controller.route('/')
def index():
    """ root page """
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
        model_array = __load_search_model(term)

    # data-table expected formatting. Unless I find a way to customize the client-side.
    model = {
        "data": model_array,
        "records_total": len(model_array)
    }
    json_output = json.dumps(model)
    return json_output

def __load_search_model(search_term):
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

@account_controller.route('/cash')
def cash_balances():
    """ Investment cash balances """
    account_names = request.form.get("accounts")
    account_names = account_names if account_names else "Assets:Investment"
    model = {
        "accounts": account_names,
        "data": []
    }
    # Selection of accounts. Display the default values the first time.
    with BookAggregate() as book_svc:
        accts_svc = AccountsAggregate(book_svc.book)
        acct = accts_svc.get_account_id_by_fullname
        acct_svc = AccountAggregate(book_svc.book, acct)
        model["data"] = acct_svc.load_cash_balances_with_children(account_names)
    # Display the report
    return render_template('account.cash.html', model=model)
