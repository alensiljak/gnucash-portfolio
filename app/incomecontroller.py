"""
Income reports
"""
from datetime import date
import dateutil
from decimal import Decimal
from flask import Blueprint, request, render_template
from piecash import Account, Split, Book
from gnucash_portfolio.lib import database

income_controller = Blueprint('income_controller', __name__,
                              url_prefix='/income')


@income_controller.route('/inperiod')
def income_in_period():
    """ Investment income in time period """
    # Check if there are parameters.
    date_from = None
    from_str = request.args.get("datefrom")
    if from_str:
        date_from = dateutil.parser.parse(from_str)
    to_str = request.args.get("dateto")
    if to_str:
        date_to = dateutil.parser.parse(to_str)

    # TODO: Allow selecting the income accounts. Save to the settings.
    income_accounts = [
        "Income:Investment"
    ]

    model = None
    if date_from:
        # load data
        with database.Database().open_book() as book:
            transactions = __load_income_in_period(
                book, income_accounts, date_from, date_to)
            model = {
                "splits": transactions,
                "datefrom": from_str,
                "dateto": to_str
            }
            output = render_template('income_in_period.html', model=model)
    else:
        output = render_template('income_in_period.html', model=model)

    return output


def __load_income_in_period(book: Book, account_fullnames: list, date_from: date, date_to: date):
    """ load income transactions in the given period """
    income_transactions = []

    # locate income account(s)
    income_accounts = __get_income_accounts(book, account_fullnames)

    # load data
    for acc in income_accounts:
        account_splits = __load_all_income_for_account(
            acc, date_from, date_to)
        income_transactions += account_splits

    return income_transactions


def __get_income_accounts(book: Book, account_fullnames: list):
    """ retrieves the account objects for the given full names """
    result = []

    for account in book.accounts:
        if account.fullname in account_fullnames:
            result.append(account)

    return result


def __load_all_income_for_account(account: Account, date_from: date, date_to: date):
    """ Loads all income in the account """
    result = []
    for split in account.splits:
        result.append(split)

    # load transactions for all child accounts
    for child in account.children:
        child_splits = __load_all_income_for_account(
            child, date_from, date_to)
        result += child_splits

    return result
