""" Stocks aggregate object """
from datetime import datetime
from decimal import Decimal
from typing import List
from sqlalchemy import desc
from piecash import Account, Book, Commodity, Price
from gnucash_portfolio.lib.aggregatebase import AggregateBase
from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate


class SecurityAggregate(AggregateBase):
    """ Stocks aggregate """
    def __init__(self, book: Book, security: Commodity):
        super(SecurityAggregate, self).__init__(book)
        # self.book = book
        self.security = security

    def get_num_shares(self) -> Decimal:
        """
        Returns the number of shares for the given security.
        It gets the number from all the accounts in the book.
        """
        today = datetime.today()
        return self.get_num_shares_on(today)

    def get_num_shares_on(self, on_date: datetime) -> Decimal:
        """ Returns the number of shares for security on (and including) the given date. """
        total_quantity = Decimal(0)
        #accts_svc = AccountsAggregate(self.book)

        for account in self.security.accounts:
            # exclude Trading accouns explicitly.
            if account.type == "TRADING":
                continue

            acct_svc = AccountAggregate(self.book, account)
            quantity = acct_svc.get_balance_on(on_date)

            total_quantity += quantity

        return total_quantity

    def get_last_available_price(self) -> Price:
        """ Finds the last available price for security """
        last_price = self.security.prices.order_by(desc(Price.date)).first()
        #return last_price.value
        return last_price

    def get_avg_price(self) -> Decimal:
        """
        Calculates the average price paid for the security.
        security = Commodity
        Returns Decimal value.
        """
        #print("Calculating stats for", security.mnemonic)
        avg_price = Decimal(0)

        #return sum([sp.quantity for sp in self.splits]) * self.sign

        price_total = Decimal(0)
        price_count = 0

        for account in self.security.accounts:
            # Ignore trading accounts.
            if account.type == "TRADING":
                continue

            for split in account.splits:
                # Don't count the non-transactions.
                if split.quantity == 0:
                    continue

                price = split.value / split.quantity
                #print(price)
                price_count += 1
                price_total += price

        #print(price_total, price_count)
        if price_count:
            avg_price = price_total / price_count
        return avg_price

    def get_dividend_accounts(self) -> List[Account]:
        """
        Finds all the distribution accounts (they are in Income group and have the same name
        as the stock symbol).
        """
        # get the stock
        #stock = selfbook.session.query(Commodity).filter(Commodity.mnemonic == symbol)

        # find all the income accounts with the same name.
        acct_query = (
            self.book.session.query(Account)
            .filter(Account.name == self.security.mnemonic)
        )
        related = acct_query.all()
        income_accounts = []
        for related_account in related:
            if related_account.fullname.startswith("Income"):
                income_accounts.append(related_account)

        return income_accounts

    def get_currency(self) -> Commodity:
        """
        Reads the currency from the latest available price information,
        assuming that all the prices are in the same currency for any symbol.
        """
        stock: Commodity = self.security
        first_price = stock.prices.first()
        if not first_price:
            raise AssertionError("Price not found for", stock.mnemonic)

        return first_price.currency

    @property
    def accounts(self):
        """ Returns the asset accounts in which the security is held """
        # use only Assets sub-accounts
        result = (
            [acct for acct in self.security.accounts if acct.fullname.startswith('Assets')]
        )
        return result


class SecuritiesAggregate(AggregateBase):
    """ Operates on security collections """
    # def __init__(self, book: Book):
    #     super(SecuritiesAggregate, self).__init__(book)
    #     pass

    def get_all(self):
        """ Loads all non-currency commodities, assuming they are stocks. """
        query = (
            self.__get_base_query()
            .order_by(Commodity.mnemonic)
        )
        return query.all()

    def get_by_symbol(self, symbol: str) -> Commodity:
        """
        Returns the commodity with the given symbol.
        If more are found, an exception will be thrown.
        """
        # handle namespace
        parts = symbol.split(':')
        if parts:
            namespace = parts[0]
            mnemonic = parts[1]
        else:
            mnemonic = symbol

        query = (
            self.__get_base_query()
            .filter(Commodity.mnemonic == mnemonic)
        )
        if parts:
            query = query.filter(Commodity.namespace == namespace)

        #return query.all()
        return query.first()

    def get_stock(self, symbol: str) -> Commodity:
        """Returns the stock/commodity object for the given symbol"""

        # Check if we have the exchange name (namespace).
        if ":" in symbol:
            # We have a namespace
            symbol_parts = symbol.split(":")
            exchange = symbol_parts[0]
            symbol = symbol_parts[1]
            security = self.book.get(Commodity, namespace=exchange, mnemonic=symbol)
        else:
            #with database.Database().open_book() as book:
            security = self.book.get(Commodity, mnemonic=symbol)

        return security

    def get_stocks(self, symbols: List[str]) -> List[Commodity]:
        """ loads stocks by symbol """
        query = (
            self.__get_base_query()
            .filter(Commodity.mnemonic.in_(symbols))
        )
        return query.all()

    def get_aggregate(self, security: Commodity) -> SecurityAggregate:
        """ Returns the aggregate for the entity """
        return SecurityAggregate(self.book, security)

    def __get_base_query(self):
        """ Returns the base query which filters out data for all queries. """
        query = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace != "CURRENCY",
                    Commodity.namespace != "template")
        )
        return query
