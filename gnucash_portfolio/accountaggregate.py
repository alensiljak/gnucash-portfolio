"""
Accounts business layer
"""
from datetime import date, datetime, timedelta
from typing import List
from decimal import Decimal
from piecash import Book, Account, Commodity, Split, Transaction
from gnucash_portfolio.currencyaggregate import CurrencyAggregate


class AccountsAggregate:
    """ Handles account collections """
    def __init__(self, book: Book):
        self.book = book


class AccountAggregate:
    """ Operations on single account """

    def __init__(self, book: Book, account: Account):
        self.account = account
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
        total = Decimal(0)
        cur_svc = CurrencyAggregate(self.book)

        # get all child accounts in a list
        cash_balances = self.load_cash_balances_with_children(root_account.fullname)
        # get the amounts
        for cur_symbol in cash_balances:
            # Currency symbol
            value = cash_balances[cur_symbol]["total"]

            if cur_symbol != currency.mnemonic:
                # TODO convert to common currency
                other_cur = cur_svc.get_currency_by_symbol(cur_symbol)
                rate = cur_svc.get_latest_rate(other_cur, currency)
                value = value * rate.value
                #print("Found", cur_symbol, value, rate.value)

            total += value

        return total


    def load_cash_balances_with_children(self, root_account_fullname: str):
        """ loads data for cash balances """
        root_account = self.get_account_by_fullname(root_account_fullname)
        accounts = self.get_all_child_accounts_as_array(root_account)

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
