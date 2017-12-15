"""
Accounts business layer
"""
from typing import List
from decimal import Decimal
from piecash import Book, Account, Commodity

class AccountAggregate:
    """ Operations on accounts """
    def __init__(self, book: Book):
        self.book = book

    def get_account_id_by_fullname(self, fullname: str) -> str:
        """ Locates the account by fullname """
        account = self.get_account_by_fullname(fullname)
        return account.guid

    def get_account_by_fullname(self, fullname: str) -> Account:
        """ Loads account by full name """
        # get all accounts and iterate, comparing the fullname. :S
        query = (
            self.book.session.query(Account)
        )
        #sql = str(query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))
        #print(sql)
        all_accounts = query.all()
        for account in all_accounts:
            if account.fullname == fullname:
                return account

    def get_all_child_accounts_as_array(self, account: Account) -> List[Account]:
        """ Returns all child accounts in a list """
        result = []
        # ignore placeholders
        if not account.placeholder:
            #continue
            result.append(account)

        for child in account.children:
            sub_accounts = self.get_all_child_accounts_as_array(child)
            result += sub_accounts

        return result

    def get_cash_balance_with_children(self, root_account: Account, currency: Commodity) -> Decimal:
        """ Loads cash balances in given currency """
        # get all child accounts in a list
        accounts = self.get_all_child_accounts_as_array(root_account)
        for account in accounts:
            # filter cash accounts only (currency accounts, not commodity)
            if account.commodity.namespace != "CURRENCY":
                continue

            print("Incomplete!", account)
