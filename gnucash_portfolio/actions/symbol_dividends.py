"""
Finds all dividends for a stock by locating all the accounts with the same name
as the symbol.
This method does not require explicit linking of distribution payments to the
stock (commodity).
"""
from decimal import Decimal
from piecash import Account, Book, Split
from gnucash_portfolio.lib import database
from gnucash_portfolio.securities import SecurityAggregate, SecuritiesAggregate


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
    """ Calculates all income for a symbol """
    svc = SecuritiesAggregate(book)
    security = svc.get_by_symbol(symbol)
    sec_svc = SecurityAggregate(book, security)
    accounts = sec_svc.get_income_accounts()
    total = Decimal(0)

    for account in accounts:
        # get all dividends.
        income = get_dividend_sum(book, account)
        total += income

    return total


def test():
    """ test method for console """
    book_path: str = input("Enter book path (or leave empty):")
    symbol: str = input("Enter symbol:")
    symbol = symbol.upper()

    if book_path:
        data = database.Database(book_path)
    else:
        data = database.Database()

    with data.open_book() as book:
        amount = get_dividend_sum_for_symbol(book, symbol)

        print("Income for", symbol, "=", amount)

if __name__ == "__main__":
    test()
