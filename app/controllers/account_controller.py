"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
import os
try: import simplejson as json
except ImportError: import json
from logging import log, DEBUG
from flask import Blueprint, request, render_template
from piecash import Account, Split, Transaction
#from django.forms.models import model_to_dict
from gnucash_portfolio.lib import datetimeutils, generic
from gnucash_portfolio.lib.settings import Settings
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate
from app.models import account_models


account_controller = Blueprint( # pylint: disable=invalid-name
    'account_controller', __name__, url_prefix='/account')


@account_controller.route('/')
def index():
    """ root page """
    return render_template('account.html')

@account_controller.route('/favourites')
def favourites():
    """ Favourite accounts """
    # TODO load list of favourite accouns
    settings = Settings()
    favourite_accts = settings.favourite_accounts

    with BookAggregate() as svc:
        accounts = svc.accounts.get_list(favourite_accts)

        model = {
            "accounts": accounts
        }
        return render_template('account.favourites.html', model=model)

# @account_controller.route('/favourites/settings')
# def favourites_settings():
#     """ Settings for favourite accounts """
#     # read settings file
#     settings = Settings()
#     account_ids = settings.favourite_accounts
#     # file_path = os.path.abspath('config/favourite_accounts.json')
#     # content = fileutils.read_text_from_file(file_path)
#     #favourites = json.loads(content)
#     model = {
#         "settings": account_ids
#     }
#     return render_template('account.favourites.settings.html', model=model)

# @account_controller.route('/favourites/settings', methods=['POST'])
# def favourites_settings_save():
#     """ Settings for favourite accounts """
#     accts = request.form.get('settings')
#     # validate json
#     json_settings = generic.validate_json(accts)
#     if not json_settings:
#         raise ValueError("invalid content")

#     # save
#     settings = Settings()
#     settings.data["favourite_accounts"] = accts
#     settings.save()

#     return render_template('settings.confirmation.html')

@account_controller.route('/list')
def all_accounts():
    """ Displays all book accounts """
    with BookAggregate() as svc:
        accounts = svc.accounts.get_all()
        # Sort by full name.
        accounts.sort(key=lambda x: x.fullname)

        model = {"accounts": accounts}
        return render_template('account.list.html', model=model)

@account_controller.route('/search')
def search():
    """ Search for an account by typing in a part of the name """
    return render_template('account.search.html')

@account_controller.route("/find")
def find():
    """
    Search for an account with the given text in the name.
    Returns JSON result. Used for datatables.
    """
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

@account_controller.route('/cash')
def cash_balances():
    """ Investment cash balances """
    account_names = request.form.get("accounts")
    account_names = account_names if account_names else "Assets:Investments"
    model = {
        "accounts": account_names,
        "data": []
    }
    # Selection of accounts. Display the default values the first time.
    with BookAggregate() as book_svc:
        accts_svc = AccountsAggregate(book_svc.book)
        acct = accts_svc.get_by_fullname(account_names)
        acct_svc = accts_svc.get_account_aggregate(acct)
        model["data"] = acct_svc.load_cash_balances_with_children(account_names)
    # Display the report
    return render_template('account.cash.html', model=model)

@account_controller.route('/transactions', methods=['GET'])
def transactions():
    """ Account transactions """
    with BookAggregate() as svc:
        in_model = model = account_models.AccountTransactionsInputModel()

        reference = __load_ref_model_for_tx(svc)

        # Check if any parameters were passed already
        account_fullname = request.args.get('acct_name')
        if account_fullname:
            acct = svc.accounts.get_by_fullname(account_fullname)
            in_model.account_id = acct.guid

        model = __load_view_model_for_tx(svc, in_model)

        return render_template(
            'account.transactions.html',
            model=model, input_model=in_model, reference=reference)

@account_controller.route('/transactions', methods=['POST'])
def transactions_post():
    """ Account transactions """
    with BookAggregate() as svc:
        reference = __load_ref_model_for_tx(svc)
        input_model = __get_input_model_for_tx()
        model = __load_view_model_for_tx(svc, input_model)

        return render_template(
            'account.transactions.html',
            model=model, input_model=input_model, reference=reference)

@account_controller.route('/<acct_id>/details')
def account_details(acct_id):
    """ Displays account details """
    with BookAggregate() as svc:
        account = svc.accounts.get_by_id(acct_id)
        agg = svc.accounts.get_account_aggregate(account)
        model = {
            "account": account,
            "quantity": agg.get_balance()
        }
        return render_template('account.details.html', model=model)

@account_controller.route('/<acct_id>/transactions')
def account_transactions(acct_id: str):
    # TODO get other parameters
    return render_template('incomplete.html')

@account_controller.route('/details/<path:fullname>')
def details(fullname):
    """ Displays account details """
    with BookAggregate() as svc:
        account = svc.accounts.get_by_fullname(fullname)

        model = account_models.AccountDetailsViewModel()
        model.account = account

        return render_template('account.details.html', model=model)

#############
# Partials
@account_controller.route('/partial/accountdetail/<account_id>')
def account_details_partial(account_id):
    with BookAggregate() as svc:
        account = svc.accounts.get_by_id(account_id)
        model = {"account": account}
        return render_template('_account.details.html', model=model)

#################
# API section

@account_controller.route('/api/search')
def search_api():
    """ searches for account by name and returns the json list of results """
    term = request.args.get('query')
    with BookAggregate() as svc:
        accounts = svc.accounts.find_by_name(term)
        #result = json.dumps(accounts)
        model_list = [{"value": account.fullname, "data": account.guid} for account in accounts]
        model_list.sort(key=lambda x: x["value"])

        result_dict = {"suggestions": model_list}
        result = json.dumps(result_dict)
    return result

@account_controller.route('/api/favourites')
def api_favourites():
    """ list of favourite accounts with balances """
    return None

######################
# Private

def __get_input_model_for_tx() -> account_models.AccountTransactionsInputModel:
    """ Parse user input or create a blank input model """
    model = account_models.AccountTransactionsInputModel()

    if not request.form:
        return model

    # read from request
    model.account_id = request.form.get('account')
    model.period = request.form.get('period')

    return model

def __load_ref_model_for_tx(svc: BookAggregate):
    """ Load reference model """
    model = account_models.AccountTransactionsRefModel()

    root_acct = svc.accounts.get_by_fullname("Assets")
    model.accounts = (
        svc.accounts.get_account_aggregate(root_acct)
        .get_all_child_accounts_as_array()
    )

    return model

def __load_view_model_for_tx(
        svc: BookAggregate,
        input_model: account_models.AccountTransactionsInputModel
    ) -> account_models.AccountTransactionsViewModel():
    """ Loads the filtered data """
    model = account_models.AccountTransactionsViewModel()
    if not input_model.account_id:
        return model

    # Load data

    # parse periods
    period = datetimeutils.parse_period(input_model.period)
    date_from = period[0]
    date_to = period[1]
    log(DEBUG, "got range: %s. Parsed to %s - %s", input_model.period, date_from, date_to)

    account = svc.accounts.get_by_id(input_model.account_id)
    model.start_balance = svc.accounts.get_account_aggregate(account).get_start_balance(date_from)
    model.end_balance = svc.accounts.get_account_aggregate(account).get_end_balance(date_to)

    query = (
        svc.book.session.query(Split)
        .join(Transaction)
        .filter(Split.account_guid == input_model.account_id)
        .filter(Transaction.post_date >= date_from)
        .filter(Transaction.post_date <= date_to)
        .order_by(Transaction.post_date)
    )
    model.splits = query.all()

    return model

def __load_search_model(search_term):
    """ Loads the data and returns an array of model objects"""
    model_array = []

    with BookAggregate() as svc:
        records = (
            svc.book.session.query(Account)
            .filter(Account.name.like(search_term))
            .all())

        for account in records:
            account_model = {
                "name": account.name,
                "fullname": account.fullname
            }
            model_array.append(account_model)

    return model_array
