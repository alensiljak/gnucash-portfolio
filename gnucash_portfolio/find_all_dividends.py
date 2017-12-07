"""
Finds all dividends for a stock by locating all the accounts with the same name
as the symbol.
This method does not require explicit linking of distribution payments to the
stock (commodity).
"""
from gnucash_portfolio.lib import database
from piecash import Account, Commodity, Book

def get_dividend_accounts(book:Book, symbol:str):
    # get the stock
    stock = book.session.query(Commodity).filter(Commodity.mnemonic == symbol)

    # find all the income accounts with the same name.
    related = book.session.query(Account).filter(Account.name == symbol).all()
    income_accounts = []
    for related_account in related:
        if related_account.fullname.startswith("Income"):
            income_accounts.append(related_account)

    return income_accounts


if __name__ == "__main__":
    book_path: str = input("Enter book path (or leave empty):")
    symbol: str = input("Enter symbol:")
    symbol = symbol.upper()

    if book_path:
        db = database.Database(book_path)
    else:
        db = database.Database()

    with db.open_book() as book:
        accounts = get_dividend_accounts(book, symbol)
        print(accounts)
