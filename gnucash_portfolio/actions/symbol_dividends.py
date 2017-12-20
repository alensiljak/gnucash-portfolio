"""
Finds all dividends for a stock by locating all the accounts with the same name
as the symbol.
This method does not require explicit linking of distribution payments to the
stock (commodity).
"""
from decimal import Decimal
from typing import List
from gnucash_portfolio.lib import database
from piecash import Account, Commodity, Book, Split
#from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate
from gnucash_portfolio.securityaggregate import SecurityAggregate, SecuritiesAggregate


def get_dividend_sum(book: Book, income_account: Account):
    """    Adds all distributions (income)    """
    splits = book.session.query(Split).filter(Split.account == income_account).all()
    dividend_sum = Decimal(0)

    for split in splits:
        dividend_sum += split.value
        # debug print split...

    # Since the income comes from the distribution account, it is marked as debit.
    return dividend_sum * (-1)


def get_dividend_sum_for_symbol(book: Book, symbol: str):
    """    Calculates all income for a symbol    """
    svc = SecuritiesAggregate(book)
    security = svc.get_by_symbol(symbol)
    sec_svc = SecurityAggregate(book, security)
    accounts = sec_svc.get_dividend_accounts()
    total = Decimal(0)

    for account in accounts:
        # get all dividends.
        income = get_dividend_sum(book, account)
        total += income

    return total


if __name__ == "__main__":
    book_path: str = input("Enter book path (or leave empty):")
    symbol: str = input("Enter symbol:")
    symbol = symbol.upper()

    if book_path:
        db = database.Database(book_path)
    else:
        db = database.Database()

    with db.open_book() as book:
        amount = get_dividend_sum_for_symbol(book, symbol)

        print("Income for", symbol, "=", amount)
