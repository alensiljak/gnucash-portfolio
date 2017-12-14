"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
import json
from decimal import Decimal
from flask import Blueprint, request, render_template
from piecash import Account
#from sqlalchemy.ext.serializer import dumps
from gnucash_portfolio import lib
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.lib import generic

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
    model = __load_cash_balances(account_names)
    # Display the report
    return render_template('account.cash.html', model=model)


# class CashBalanceRow:
#     """ Represents a row in the cash balances report """
#     def __init__(self):
#         self.name = None
#         self.fullname = None
#         self.currency = None
#         self.balance = None


def __load_cash_balances(root_account_name: str):
    """ loads data for cash balances """
    with Database().open_book() as book:
        root_account_id = lib.accounts.get_account_id_by_fullname(book, root_account_name)
        query = (
            book.session.query(Account)
            .filter(Account.guid == root_account_id)
        )
        # Check the generated SQL
        #generic.print_sql(query)
        root_account = query.one()

        # get cash balances
        accounts = lib.accounts.get_all_child_accounts_as_array(root_account)

        model = {}
        for account in accounts:
            # filter currencies only
            if account.commodity.namespace != "CURRENCY":
                continue

            # separate per currency
            currency = account.commodity.mnemonic

            if not currency in model:
                # Add the currency branch.
                currency_record = {
                    "name": currency,
                    "total": 0,
                    "rows": []
                }
                # Append to the root.
                model[currency] = currency_record

            row = {
                "name": account.name,
                "fullname": account.fullname,
                "currency": currency,
                "balance": account.get_balance()
            }
            model[currency]["rows"].append(row)

            # add to total
            total = Decimal(model[currency]["total"])
            total += account.get_balance()
            model[currency]["total"] = total

    return model
