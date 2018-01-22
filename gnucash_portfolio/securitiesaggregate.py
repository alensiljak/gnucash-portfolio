""" Stocks aggregate object
This should include all non-currency commodities.
Accounts should be only accounts that hold these commodities.
"""
import datetime
from decimal import Decimal
from logging import log, DEBUG
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from piecash import Account, Book, Commodity, Price, Split
from gnucash_portfolio.lib import datetimeutils
from gnucash_portfolio.lib.aggregatebase import AggregateBase
from gnucash_portfolio.accountaggregate import AccountAggregate # AccountsAggregate
from gnucash_portfolio.currencyaggregate import CurrenciesAggregate


class SecurityAggregate(AggregateBase):
    """ Stocks aggregate """
    def __init__(self, book: Book, security: Commodity):
        super(SecurityAggregate, self).__init__(book)
        # self.book = book
        self.security = security

    def create_price(self):
        """ Create price for security """
        pass

    def get_quantity(self) -> Decimal:
        """
        Returns the number of shares for the given security.
        It gets the number from all the accounts in the book.
        """
        # Use today's date but reset hour and lower.
        today = datetimeutils.today_datetime()
        today = datetimeutils.end_of_day(today)
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

    def get_value(self) -> Decimal:
        """ Returns the current value of stocks """
        quantity = self.get_quantity()
        price = self.get_last_available_price()
        if not price:
            # raise ValueError("no price found for", self.full_symbol)
            return Decimal(0)

        value = quantity * price.value
        return value

    def get_value_in_base_currency(self) -> Decimal:
        """ Calculates the value of security holdings in base currency """
        # check if the currency is the base currency.
        amt_orig = self.get_value()
        # Security currency
        sec_cur = self.get_currency()
        #base_cur = self.book.default_currency
        cur_svc = CurrenciesAggregate(self.book)
        base_cur = cur_svc.get_default_currency()

        if sec_cur == base_cur:
            return amt_orig

        # otherwise recalculate
        single_svc = cur_svc.get_currency_aggregate(sec_cur)
        rate = single_svc.get_latest_rate(base_cur)

        result = amt_orig * rate.value
        return result

    def get_last_available_price(self) -> Price:
        """ Finds the last available price for security """
        query = (
            self.security.prices
            .order_by(desc(Price.date))
        )
        last_price = query.first()
        #return last_price.value
        return last_price

    def get_avg_price(self) -> Decimal:
        """
        Calculates the average price paid for the security.
        security = Commodity
        Returns Decimal value.
        """
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
        last_price = self.get_last_available_price()
        if not last_price:
            return None

        return last_price.currency

    def get_distributions(self):
        pass

    def get_income_accounts(self) -> List[Account]:
        """
        Returns all income accounts for this security.
        Income accounts are accounts not under Trading, expressed in currency, and
        having the same name as the mnemonic.
        They should be under Assets but this requires a recursive SQL query.
        """
        trading = self.book.trading_account(self.security)
        # log(DEBUG, "trading account = %s, %s", trading.fullname, trading.guid)
        parent_alias = aliased(Account)
        query = (
            self.book.session.query(Account)
            .join(Commodity)
            .join(parent_alias, Account.parent)
            .filter(Account.name == self.security.mnemonic,
                    Commodity.namespace == "CURRENCY",
                    parent_alias.parent_guid != trading.guid)
        )
        #generic.print_sql(query)
        return query.all()

    def get_prices(self) -> List[Price]:
        """ Returns all available prices for security """
        return self.security.prices.order_by(Price.date)

    def get_total_paid(self) -> Decimal:
        """ Returns the total amount paid, in currency, for the stocks owned """
        # TODO use lots to find only the remaining stocks and remove the sold ones from calculation?

        query = (
            self.get_splits_query()
        )
        splits = query.all()
        # log(DEBUG, splits)

        total = Decimal(0)
        for split in splits:
            total += split.value

        return total

    def get_splits_query(self):
        """ Returns the query for all splits for this security """
        query = (
            self.book.session.query(Split)
            .join(Account)
            .filter(Account.type != "TRADING")
            .filter(Account.commodity_guid == self.security.guid)
        )
        return query

    ######################
    # Properties

    @property
    def accounts(self):
        """ Returns the asset accounts in which the security is held """
        # use only Assets sub-accounts
        result = (
            [acct for acct in self.security.accounts if acct.fullname.startswith('Assets')]
        )
        return result

    @property
    def full_symbol(self):
        """ Returns the full symbol (namespace + symbol) """
        return self.security.namespace + ":" + self.security.mnemonic


class SecuritiesAggregate(AggregateBase):
    """ Operates on security collections """
    # def __init__(self, book: Book):
    #     super(SecuritiesAggregate, self).__init__(book)
    #     pass

    def find(self, search_term: str) -> List[Commodity]:
        """ Searches for security by part of the name """
        query = (
            self.query
            .filter(Commodity.mnemonic.like('%' + search_term + '%') |
                    Commodity.fullname.like('%' + search_term + '%'))
        )
        return query.all()

    def get_all(self):
        """ Loads all non-currency commodities, assuming they are stocks. """
        query = (
            self.query
            .order_by(Commodity.mnemonic)
        )
        return query.all()

    def get_by_symbol(self, symbol: str) -> Commodity:
        """
        Returns the commodity with the given symbol.
        If more are found, an exception will be thrown.
        """
        # handle namespace. Accept GnuCash and Yahoo-style symbols.
        full_symbol = self.__parse_gc_symbol(symbol)

        query = (
            self.query
            .filter(Commodity.mnemonic == full_symbol["mnemonic"])
        )
        if full_symbol["namespace"]:
            query = query.filter(Commodity.namespace == full_symbol["namespace"])

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
            self.query
            .filter(Commodity.mnemonic.in_(symbols))
        )
        return query.all()

    def get_aggregate(self, security: Commodity) -> SecurityAggregate:
        """ Returns the aggregate for the entity """
        return SecurityAggregate(self.book, security)

    def get_aggregate_for_symbol(self, symbol: str) -> SecurityAggregate:
        """ Returns the aggregate for the security found by full symbol """
        security = self.get_by_symbol(symbol)
        return self.get_aggregate(security)

    @property
    def query(self):
        """ Returns the base query which filters out data for all queries. """
        query = (
            self.book.session.query(Commodity)
            .filter(Commodity.namespace != "CURRENCY",
                    Commodity.namespace != "template")
        )
        return query

    #######################################
    # Private

    def __parse_gc_symbol(self, gc_symbol: str):
        """ Parse GnuCash-style symbol "namespace:mnemonic" """
        result = {
            "namespace": None,
            "mnemonic": None
        }

        parts = gc_symbol.split(':')
        if len(parts) > 1:
            result["namespace"] = parts[0]
            result["mnemonic"] = parts[1]
        else:
            result["mnemonic"] = gc_symbol

        return result
