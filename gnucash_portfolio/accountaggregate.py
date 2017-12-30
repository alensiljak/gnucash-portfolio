"""
Accounts business layer.
Accounts should only be Asset, Bank, Mutual, and Stock in the context of Portfolio?
"""
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import List
from decimal import Decimal
from logging import log, DEBUG
from piecash import Book, Account, Commodity, Split, Transaction
from gnucash_portfolio.lib import datetimeutils
from gnucash_portfolio.lib.aggregatebase import AggregateBase
from gnucash_portfolio.currencyaggregate import CurrencyAggregate, CurrenciesAggregate


class AccountType(Enum):
    """ Account Types """
    ROOT = auto()
    ASSET = auto()
    LIABILITY = auto()
    EXPENSE = auto()
    INCOME = auto()
    TRADING = auto()
    MUTUAL = auto()
    STOCK = auto()
    BANK = auto()


class AccountAggregate(AggregateBase):
    """ Operations on single account """

    def __init__(self, book: Book, account: Account):
        super(AccountAggregate, self).__init__(book)

        self.account = account
        #self.book = book

    def get_all_child_accounts_as_array(self) -> List[Account]:
        """ Returns the whole tree of child accounts in a list """
        return self.__get_all_child_accounts_as_array(self.account)

    def get_cash_balance_with_children(self, root_account: Account, currency: Commodity) -> Decimal:
        """
        Loads cash balances in given currency.
        currency: the currency for the total
        """
        total = Decimal(0)
        svc = CurrenciesAggregate(self.book)

        # get all child accounts in a list
        cash_balances = self.load_cash_balances_with_children(root_account.fullname)
        # get the amounts
        for cur_symbol in cash_balances:
            # Currency symbol
            value = cash_balances[cur_symbol]["total"]

            if cur_symbol != currency.mnemonic:
                # Convert the amount to the given currency.
                other_cur = svc.get_by_symbol(cur_symbol)

                #log(DEBUG, "loading %s/%s rate", currency.mnemonic, other_cur.mnemonic)

                cur_svc = svc.get_currency_aggregate(other_cur)

                rate = cur_svc.get_latest_rate(currency)
                value = value * rate.value

            total += value

        return total

    def load_cash_balances_with_children(self, root_account_fullname: str):
        """ loads data for cash balances """
        svc = AccountsAggregate(self.book)
        root_account = svc.get_by_fullname(root_account_fullname)
        if not root_account:
            raise ValueError("Account not found", root_account_fullname)
        accounts = self.__get_all_child_accounts_as_array(root_account)

        # read cash balances
        model = {}
        for account in accounts:
            if account.commodity.namespace != "CURRENCY":
                continue

            # separate per currency
            currency_symbol = account.commodity.mnemonic

            if not currency_symbol in model:
                # Add the currency branch.
                currency_record = {
                    "name": currency_symbol,
                    "total": 0,
                    "rows": []
                }
                # Append to the root.
                model[currency_symbol] = currency_record
            else:
                currency_record = model[currency_symbol]

            #acct_svc = AccountAggregate(self.book, account)
            balance = account.get_balance()
            row = {
                "name": account.name,
                "fullname": account.fullname,
                "currency": currency_symbol,
                "balance": balance
            }
            currency_record["rows"].append(row)

            # add to total
            total = Decimal(currency_record["total"])
            total += balance
            currency_record["total"] = total

        return model

    def get_start_balance(self, before: date) -> Decimal:
        """ Calculates account balance """
        # create a new date without hours
        date_corrected = datetimeutils.start_of_day(before)
        # now subtract 1 second.
        date_corrected -= timedelta(seconds=1)
        #log(DEBUG, "getting balance on %s", date_corrected)
        return self.get_balance_on(date_corrected)

    def get_end_balance(self, after: date) -> Decimal:
        """ Calculates account balance """
        # create a new date without hours
        date_corrected = datetimeutils.end_of_day(after)
        #log(DEBUG, "getting balance on %s", date_corrected)
        return self.get_balance_on(date_corrected)

    def get_balance_on(self, on_date: datetime) -> Decimal:
        """ Returns the balance on (and including) a certain date """
        total = Decimal(0)

        splits = self.get_splits_up_to(on_date)

        for split in splits:
            total += split.quantity * self.account.sign
        return total

    def get_splits_up_to(self, date_to: datetime) -> List[Split]:
        """ returns splits only up to the given date """
        query = (
            self.book.session.query(Split)
            .join(Transaction)
            .filter(Split.account == self.account,
                    Transaction.post_date <= date_to)
        )
        return query.all()

    ####################
    # Private

    def __get_all_child_accounts_as_array(self, account: Account) -> List[Account]:
        """ Returns the whole tree of child accounts in a list """
        result = []
        # ignore placeholders
        if not account.placeholder:
            #continue
            result.append(account)

        for child in account.children:
            sub_accounts = self.__get_all_child_accounts_as_array(child)
            result += sub_accounts

        return result


class AccountsAggregate(AggregateBase):
    """ Handles account collections """
    def __init__(self, book: Book):
        super(AccountsAggregate, self).__init__(book)
        #self.book = book
        pass

    def find_by_name(self, term: str) -> List[Account]:
        """ Search for account by part of the name """
        query = (
            self.query
            .filter(Account.name.like('%' + term + '%'))
            .order_by(Account.name)
        )
        return query.all()

    def get_by_fullname(self, fullname: str) -> Account:
        """ Loads account by full name """
        # get all accounts and iterate, comparing the fullname. :S
        query = (
            self.book.session.query(Account)
        )
        #sql = str(query.statement.compile(dialect=sqlite.dialect(), 
        # compile_kwargs={"literal_binds": True}))
        #print(sql)
        all_accounts = query.all()
        for account in all_accounts:
            if account.fullname == fullname:
                return account

    def get_account_id_by_fullname(self, fullname: str) -> str:
        """ Locates the account by fullname """
        account = self.get_by_fullname(fullname)
        return account.guid

    def get_all_children(self, fullname: str) -> List[Account]:
        """ Returns the whole child account tree for the account with the given full name """
        # find the account by fullname
        root_acct = self.get_by_fullname(fullname)
        if not root_acct:
            raise NameError("Account not found in book!")

        acct_agg = self.get_account_aggregate(root_acct)
        acct_agg.get_all_child_accounts_as_array()
        for child in root_acct.children:
            log(DEBUG, "found child %s", child.fullname)
        return

    def get_all(self) -> List[Account]:
        """ Returns all book accounts as a list, excluding templates. """
        return [account for account in self.book.accounts if account.parent.name != "Template Root"]

    def get_account_aggregate(self, account: Account) -> AccountAggregate:
        """ Returns account aggregate """
        return AccountAggregate(self.book, account)

    def get_by_id(self, acct_id) -> Account:
        """ Loads an account entity """
        return self.book.get(Account, guid=acct_id)

    def get_by_name(self, name: str) -> List[Account]:
        """ Searches accounts by name """
        #return self.query.filter(Account.name == name).all()
        return self.get_by_name_from(self.book.root, name)

    def get_by_name_from(self, root: Account, name: str) -> List[Account]:
        """ Searches child accounts by name, starting from the given account """
        result = []

        if root.name == name:
            result.append(root)

        for child in root.children:
            child_results = self.get_by_name_from(child, name)
            result += child_results

        return result

    def get_list(self, ids: List[str]) -> List[Account]:
        """ Loads accounts by the ids passed as an argument """
        query = (
            self.query
            .filter(Account.guid.in_(ids))
        )
        return query.all()

    @property
    def query(self):
        """ Main accounts query """
        query = (
            self.book.session.query(Account)
            .filter(Account.type != AccountType.ROOT.name)
        )
        return query
