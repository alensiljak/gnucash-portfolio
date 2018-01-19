"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
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
from app.models.account_models import (
    AccountDetailsViewModel, AccountTransactionsInputModel,
    AccountTransactionsViewModel, AccountTransactionsRefModel)


account_controller = Blueprint(  # pylint: disable=invalid-name
    'account_controller', __name__, url_prefix='/account')


@account_controller.route('/')
def index():
    """ root page """
    return render_template('account.html')


@account_controller.route('/favourites')
def favourites():
    """ Favourite accounts """
    with BookAggregate() as svc:
        model = __load_favourite_accounts_model(svc)

        return render_template('account.favourites.html', model=model)


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
        model["data"] = acct_svc.load_cash_balances_with_children(
            account_names)
    # Display the report
    return render_template('account.cash.html', model=model)

@account_controller.route('/splits', methods=['GET'])
def transactions():
    """ Account transactions """
    with BookAggregate() as svc:
        in_model = model = AccountTransactionsInputModel()

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

@account_controller.route('/splits', methods=['POST'])
def transactions_post():
    """ Account transactions """
    input_model = __get_input_model_for_tx()
    return account_splits(input_model.account_id)

@account_controller.route('/<acct_id>/details')
def account_details(acct_id):
    """ Displays account details """
    with BookAggregate() as svc:
        model = __load_account_details_model(svc, acct_id)

        return render_template('account.details.html', model=model)

@account_controller.route('/<acct_id>/splits')
def account_splits(acct_id: str):
    """ Displays account transactions with splits in period """
    input_model = __get_input_model_for_tx()
    input_model.account_id = acct_id

    with BookAggregate() as svc:
        reference = __load_ref_model_for_tx(svc)
        model = __load_view_model_for_tx(svc, input_model)

        return render_template(
            'account.transactions.html',
            model=model, input_model=input_model, reference=reference)

@account_controller.route('/transactions')
def account_transactions():
    """ Lists only transactions """
    return render_template('account.transactions.vue.html')

@account_controller.route('/details/<path:fullname>')
def details(fullname):
    """ Displays account details """
    with BookAggregate() as svc:
        account = svc.accounts.get_by_fullname(fullname)

        model = __load_account_details_model(svc, account.guid)

        return render_template('account.details.html', model=model)

#############
# Partials

@account_controller.route('/partial/accountdetail/<account_id>')
def account_details_partial(account_id):
    with BookAggregate() as svc:
        model = __load_account_details_model(svc, account_id)

        return render_template('_account.details.html', model=model)

@account_controller.route('/partial/favourites')
def api_favourites():
    """ list of favourite accounts with balances """
    with BookAggregate() as svc:
        model = __load_favourite_accounts_model(svc)

        return render_template('_account.favourites.html', model=model)

#################
# API section

@account_controller.route('/api/search')
def search_api():
    """ searches for account by name and returns the json list of results """
    term = request.args.get('query')
    with BookAggregate() as svc:
        accounts = svc.accounts.find_by_name(term)
        #result = json.dumps(accounts)
        model_list = [{"name": account.fullname, "id": account.guid}
                      for account in accounts]
        model_list.sort(key=lambda x: x["name"])

        result_dict = {"suggestions": model_list}
        result = json.dumps(result_dict)
    return result

@account_controller.route('/api/search_autocomplete')
def api_search_autocomplete():
    """ format the output for autocomplete. Client-side customization does not work for some reason. """
    term = request.args.get('query')
    with BookAggregate() as svc:
        accounts = svc.accounts.find_by_name(term)
        #result = json.dumps(accounts)
        model_list = [{"value": account.fullname, "data": account.guid}
                      for account in accounts]
        model_list.sort(key=lambda x: x["value"])

        result_dict = {"suggestions": model_list}
        result = json.dumps(result_dict)
    return result

@account_controller.route('/api/transactions')
def api_transactions():
    """ Returns account transactions """
    # get parameters
    dateFromStr = request.args.get("dateFrom")
    dateFrom = datetimeutils.parse_iso_date(dateFromStr).date()
    dateToStr = request.args.get("dateTo")
    dateTo = datetimeutils.parse_iso_date(dateToStr).date()
    account_id = request.args.get("account")

    # get data
    with BookAggregate() as svc:
        acc_agg = svc.accounts.get_aggregate_by_id(account_id)
        txs = acc_agg.get_transactions(dateFrom, dateTo)
        records = []

        # return results
        model = {
            "accountName": acc_agg.account.fullname,
            "startBalance": acc_agg.get_start_balance(dateFrom),
            "endBalance": acc_agg.get_end_balance(dateTo),
            "transactions": []
        }

        for tx in txs:
            this_split = [split for split in tx.splits if split.transaction == tx][0]
            records.append({
                "date": tx.post_date.strftime("%Y-%m-%d"),
                "description": tx.description,
                "notes": tx.notes,
                "value": this_split.value,
                "quantity": this_split.quantity
            })
        model["transactions"] = records

    result = json.dumps(model)
    return result

######################
# Private

def __get_input_model_for_tx() -> AccountTransactionsInputModel:
    """ Parse user input or create a blank input model """
    model = AccountTransactionsInputModel()

    if request.args:
        # model.account_id = request.args.get('account')
        model.period = request.args.get('period')

    if request.form:
        # read from request
        model.account_id = request.form.get('account')
        model.period = request.form.get('period')

    return model

def __load_ref_model_for_tx(svc: BookAggregate):
    """ Load reference model """
    model = AccountTransactionsRefModel()

    root_acct = svc.accounts.get_by_fullname("Assets")
    model.accounts = (
        svc.accounts.get_account_aggregate(root_acct)
        .get_all_child_accounts_as_array()
    )

    return model

def __load_view_model_for_tx(
    svc: BookAggregate,
    input_model: AccountTransactionsInputModel
) -> AccountTransactionsViewModel():
    """ Loads the filtered data """
    model = AccountTransactionsViewModel()
    if not input_model.account_id:
        return model

    # Load data

    # parse periods
    period = datetimeutils.parse_period(input_model.period)
    date_from = period[0]
    date_to = period[1]
    log(DEBUG, "got range: %s. Parsed to %s - %s",
        input_model.period, date_from, date_to)

    account = svc.accounts.get_by_id(input_model.account_id)
    model.start_balance = svc.accounts.get_account_aggregate(
        account).get_start_balance(date_from)
    model.end_balance = svc.accounts.get_account_aggregate(
        account).get_end_balance(date_to)

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

def __load_account_details_model(svc: BookAggregate, acct_id: str) -> AccountDetailsViewModel:
    """ Loads account details view model """
    agg = svc.accounts.get_aggregate_by_id(acct_id)

    model = AccountDetailsViewModel()
    model.account = agg.account
    model.quantity = agg.get_balance()

    return model

def __load_favourite_accounts_model(svc: BookAggregate):
    """ Loads favourite accounts view model """
    settings = Settings()
    favourite_accts = settings.favourite_accounts
    accounts = svc.accounts.get_list(favourite_accts)
    # sort by name
    accounts.sort(key=lambda acc: acc.name)

    model = {
        "accounts": accounts
    }
    return model
