""" Income reports """
from typing import List
from logging import log, DEBUG
from datetime import date, timedelta
from flask import Blueprint, request, render_template
from piecash import Account, Commodity, Split, Book, Transaction
from gnucash_portfolio.bookaggregate import BookAggregate
from app.models.distribution_models import DistributionsInputModel, DistributionsViewModel

distribution_controller = Blueprint( # pylint: disable=invalid-name
    'distribution_controller', __name__, url_prefix='/distributions')

@distribution_controller.route('/')
def income_in_period():
    """ Investment income in time period, parameters """

    # TODO get income accounts from settings?
    # TODO add collapsible indicator icon to the filter header
    # https://stackoverflow.com/questions/18325779/bootstrap-3-collapse-show-state-with-chevron-icon

    return render_template('distributions.html', model=None, in_model=None)

@distribution_controller.route('/', methods=['POST'])
def income_in_period_data():
    """ Displays the results """
    in_model = __get_input_model()

    # load data
    with BookAggregate() as svc:
        model = __get_model_inperiod(in_model, svc)
        return render_template('distributions.html', model=model, in_model=in_model)

@distribution_controller.route('/<symbol>', methods=['GET'])
def for_security(symbol):
    """ Income for specific security. Symbol must be the full symbol,
    including the exchange (namespace). """
    #log(DEBUG, "symbol = %s", symbol)
    with BookAggregate() as svc:
        in_model = DistributionsInputModel()
        sec_agg = svc.securities.get_aggregate_for_symbol(symbol)
        accounts = [account.fullname for account in sec_agg.get_income_accounts()]
        in_model.accounts = ','.join(accounts)
        log(DEBUG, "accounts = %s", in_model.accounts)

        model = __get_model_inperiod(in_model, svc)

        return render_template('distributions.html', model=model, in_model=in_model)

###################
# Private

def __get_model_inperiod(in_model, svc: BookAggregate) -> DistributionsViewModel:
    """ Creates the data model for the prices in period """
    model = DistributionsViewModel()

    # income accounts
    account_names = in_model.accounts.split(",")

    account_ids = __get_income_account_ids(svc.book, account_names)
    splits = __load_income_in_period_query(
        svc.book, account_ids, in_model)

    model.splits = splits

    return model

def __get_input_model() -> DistributionsInputModel:
    """ Parses user input into a data-transfer object (DTO) """
    model = DistributionsInputModel()
    # request.args.get

    accounts = request.form.get("accounts")
    if accounts:
        model.accounts = accounts

    period = request.form.get("period")
    if period:
        model.period = period

    currency = request.form.get("currency")
    if currency:
        model.currency = currency

    return model

def __load_income_in_period(
        book: Book, account_fullnames: List[str], date_from: date, date_to: date):
    """ load income transactions in the given period """
    income_transactions = []

    # locate income account(s)
    income_accounts = __get_accounts_by_name(book, account_fullnames)

    # load data
    for acc in income_accounts:
        account_splits = __load_all_income_for_account(
            acc, date_from, date_to)
        income_transactions += account_splits

    return income_transactions

def __get_accounts_by_name(book: Book, account_fullnames: List[str]) -> List[Account]:
    """ retrieves the account objects for the given full names """
    result = []

    for account in book.accounts:
        if account.fullname in account_fullnames:
            result.append(account)

    return result

def __get_ids(accounts: List[Account]):
    """ extracts only the ids from the account list """
    return [o.guid for o in accounts]

def __get_income_account_ids(book: Book, account_names: List[str]) -> List[str]:
    """ Loads all income account ids """
    accounts = __get_accounts_by_name(book, account_names)
    ids = []

    for account in accounts:
        child_ids = __get_children_ids(account)
        ids += child_ids

    return ids

def __get_children_ids(account: Account) -> List[str]:
    """ recursive function that loads ids from all child accounts in the tree """
    ids = []

    if not account.placeholder:
        ids.append(account.guid)

    for child in account.children:
        child_ids = __get_children_ids(child)
        ids += child_ids
    return ids

def __load_all_income_for_account(account: Account, date_from: date, date_to: date):
    """ Loads all income in the account """
    result = []
    splits_in_period = account.splits()
    for split in splits_in_period:
        result.append(split)

    # load transactions for all child accounts
    for child in account.children:
        child_splits = __load_all_income_for_account(
            child, date_from, date_to)
        result += child_splits

    return result

def __load_income_in_period_query(
        book: Book, account_ids: List[hex], in_model) -> List[Split]:
    """ Load all data by using the query directly """

    date_from = in_model.date_from
    date_to = in_model.date_to
    # increase the destination date
    date_to += timedelta(days=1)

    query = (book.query(Split)
             .join(Transaction)
             .join(Account)
             .filter(Transaction.post_date >= date_from, Transaction.post_date <= date_to,
                     Account.guid.in_(account_ids))
             .order_by(Transaction.post_date)
            )

    if in_model.currency:
        query = (query
                 .join(Commodity)
                 .filter(Commodity.mnemonic == in_model.currency)
                )

    return query.all()
