"""
Simple piecash script that reads accounts.
https://github.com/sdementen/piecash
"""
import piecash
with piecash.open_book("../test.gnucash") as book:
    # get default currency of book
    print( book.default_currency )  # ==> Commodity<CURRENCY:EUR>

    # iterating over all splits in all books and print the transaction description:
    for acc in book.accounts:
        for sp in acc.splits:
            print(sp.transaction.description)

#