"""
Income reports
"""
from typing import List
from datetime import date
import dateutil
#from decimal import Decimal
from flask import Blueprint, request, render_template
#from sqlalchemy.dialects import sqlite
from piecash import Account, Split, Book, Transaction
from gnucash_portfolio.lib import database

income_controller = Blueprint('income_controller', __name__,
                              url_prefix='/income')


@income_controller.route('/inperiod')
def income_in_period():
    """ Investment income in time period """
    input_model = __get_input_model()

    # Allow selecting the income accounts.
    # TODO Save to the settings?
    income_accounts = [
        "Income:Investment"
    ]

    model = {}
    if "date_from" in input_model:
        model = {
            "datefrom": input_model["date_from_str"],
            "dateto": input_model["date_to_str"]
        }
        # load data
        with database.Database().open_book() as book:
            #            splits = __load_income_in_period(
            #                book, income_accounts, date_from, date_to)
            # Sort by date
            #            splits.sort(key=lambda split: split.transaction.post_date)

            account_ids = __get_income_account_ids(book, income_accounts)
            splits = __load_income_in_period_query(book, account_ids,
                                                   input_model["date_from"], input_model["date_to"])

            model["splits"] = splits
            output = render_template('income_in_period.html', model=model)
    else:
        output = render_template('income_in_period.html', model=model)

    return output


def __get_input_model():
    """ Parses user input """
    model = {}

    from_str = request.args.get("datefrom")
    if from_str:
        model["date_from"] = dateutil.parser.parse(from_str)
        model["date_from_str"] = from_str

    to_str = request.args.get("dateto")
    if to_str:
        model["date_to"] = dateutil.parser.parse(to_str)
        model["date_to_str"] = to_str

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
        book: Book, account_ids: List[hex],
        date_from: date, date_to: date) -> List[Split]:
    """ Load all data by using the query directly """
    query = (book.query(Split)
             .join(Transaction)
             .join(Account)
             .filter(Transaction.post_date >= date_from, Transaction.post_date <= date_to,
                     Account.guid.in_(account_ids))
             .order_by(Transaction.post_date)
            )
    # Check the generated SQL
#    sql = str(query.statement.compile(dialect=sqlite.dialect(),
#       compile_kwargs={"literal_binds": True}))
    return query.all()
