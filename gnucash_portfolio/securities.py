"""
Stocks aggregate object
This should include all non-currency commodities.
Accounts should be only accounts that hold these commodities.
"""
import datetime
from decimal import Decimal
from typing import List

from piecash import Account, AccountType, Book, Commodity, Split, Transaction
from sqlalchemy import desc
from pricedb import PriceDbApplication, PriceModel, SecuritySymbol

from gnucash_portfolio.accounts import AccountAggregate
from gnucash_portfolio.currencies import CurrenciesAggregate
from gnucash_portfolio.lib.aggregatebase import AggregateBase
from gnucash_portfolio.mappers import splitmapper
from gnucash_portfolio.model.split_model import SplitModel


class SecurityAggregate(AggregateBase):
    """ Stocks aggregate """
    def __init__(self, book: Book, security: Commodity):
        super(SecurityAggregate, self).__init__(book)
        self.security = security
        # cache of holding accounts
        self.__holding_accounts = None

    def create_price(self):
        """ Create price for security """
        # pass
        raise NotImplementedError()

    def get_avg_price(self):
        """ Returns the default avg. price """
        # Use statistical average of the price until fifo calculation is complete.
        # return self.get_avg_price_stat()
        return self.get_avg_price_fifo()

    def get_avg_price_stat(self) -> Decimal:
        """
        Calculates the statistical average price for the security,
        by averaging only the prices paid. Very simple first implementation.
        """
        avg_price = Decimal(0)

        price_total = Decimal(0)
        price_count = 0

        for account in self.security.accounts:
            # Ignore trading accounts.
            if account.type == AccountType.TRADING.name:
                continue

            for split in account.splits:
                # Don't count the non-transactions.
                if split.quantity == 0:
                    continue

                price = split.value / split.quantity
                price_count += 1
                price_total += price

        if price_count:
            avg_price = price_total / price_count
        return avg_price

    def get_avg_price_fifo(self) -> Decimal:
        """
        Calculates the average price paid for the security.
        security = Commodity
        Returns Decimal value.
        """
        balance = self.get_quantity()
        if not balance:
            return Decimal(0)

        paid = Decimal(0)
        accounts = self.get_holding_accounts()
        # get unused splits (quantity and total paid) per account.
        for account in accounts:
            splits = self.get_available_splits_for_account(account)

            for split in splits:
                paid += split.value

        avg_price = paid / balance
        return avg_price

    def get_available_splits_for_account(self, account: Account) -> List[Split]:
        """ Returns all unused splits in the account. Used for the calculation of avg.price.
        The split that has been partially used will have its quantity reduced to available
        quantity only. """
        available_splits = []
        # get all purchase splits in the account
        query = (
            self.get_splits_query()
            .filter(Split.account == account)
        )
        buy_splits = (
            query.filter(Split.quantity > 0)
            .join(Transaction)
            .order_by(desc(Transaction.post_date))
        ).all()
        buy_q = sum(split.quantity for split in buy_splits)
        sell_splits = query.filter(Split.quantity < 0).all()
        sell_q = sum(split.quantity for split in sell_splits)
        balance = buy_q + sell_q
        if balance == 0:
            return available_splits

        for real_split in buy_splits:
            split = splitmapper.map_split(real_split, SplitModel())

            if split.quantity < balance:
                # take this split and reduce the balance.
                balance -= split.quantity
            else:
                # This is the last split.
                price = split.value / split.quantity
                # Take only the remaining quantity.
                split.quantity -= balance
                # Also adjust the value for easier calculation elsewhere.
                split.value = balance * price
                # The remaining balance is now distributed into splits.
                balance = 0
            # add to the collection.
            available_splits.append(split)
            if balance == 0:
                break

        return available_splits

    def get_num_shares(self) -> Decimal:
        """ Returns the number of shares at this time """
        from pydatum import Datum
        today = Datum().today()
        return self.get_num_shares_on(today)

    def get_num_shares_on(self, on_date: datetime) -> Decimal:
        """ Returns the number of shares for security on (and including) the given date. """
        total_quantity = Decimal(0)

        accounts = self.get_holding_accounts()
        for account in accounts:
            acct_svc = AccountAggregate(self.book, account)
            quantity = acct_svc.get_balance_on(on_date)

            total_quantity += quantity

        return total_quantity

    def get_last_available_price(self) -> PriceModel:
        """ Finds the last available price for security. Uses PriceDb. """
        price_db = PriceDbApplication()
        symbol = SecuritySymbol(self.security.namespace, self.security.mnemonic)
        result = price_db.get_latest_price(symbol)
        return result

    def get_currency(self) -> str:
        """
        Reads the currency from the latest available price information,
        assuming that all the prices are in the same currency for any symbol.
        """
        last_price = self.get_last_available_price()
        if not last_price:
            return None

        # logging.debug(f"currency is {last_price.currency}")
        return last_price.currency

    def get_holding_accounts(self) -> List[Account]:
        """ Returns the (cached) list of holding accounts """
        if not self.__holding_accounts:
            self.__holding_accounts = self.__get_holding_accounts_query().all()

        return self.__holding_accounts

    def __get_holding_accounts_query(self):
        """ Returns all holding accounts, except Trading accounts. """
        query = (
            self.book.session.query(Account)
            .filter(Account.commodity == self.security)
            .filter(Account.type != AccountType.trading.value)
        )
        # generic.print_sql(query)
        return query

    def get_income_accounts(self) -> List[Account]:
        """
        Returns all income accounts for this security.
        Income accounts are accounts not under Trading, expressed in currency, and
        having the same name as the mnemonic.
        They should be under Assets but this requires a recursive SQL query.
        """
        # trading = self.book.trading_account(self.security)
        # log(DEBUG, "trading account = %s, %s", trading.fullname, trading.guid)

        # Example on how to self-link, i.e. parent account, using alias.
        # parent_alias = aliased(Account)
            # .join(parent_alias, Account.parent)
        # parent_alias.parent_guid != trading.guid

        query = (
            self.book.session.query(Account)
            .join(Commodity)
            .filter(Account.name == self.security.mnemonic)
            .filter(Commodity.namespace == "CURRENCY")
            # .filter(Account.type != "TRADING")
            .filter(Account.type == AccountType.income.value)
        )
        # generic.print_sql(query)
        return query.all()

    def get_income_total(self) -> Decimal:
        """ Sum of all income = sum of balances of all income accounts. """
        accounts = self.get_income_accounts()
        # log(DEBUG, "income accounts: %s", accounts)
        income = Decimal(0)
        for acct in accounts:
            income += acct.get_balance()
        return income

    def get_income_in_period(self, start: datetime, end: datetime) -> Decimal:
        """ Returns all income in the given period """
        # get_income_in_account_period
        pass

    def get_prices(self) -> List[PriceModel]:
        """ Returns all available prices for security """
        # return self.security.prices.order_by(Price.date)
        from pricedb.dal import Price

        pricedb = PriceDbApplication()
        repo = pricedb.get_price_repository()
        query = (repo.query(Price)
            .filter(Price.namespace == self.security.namespace)
            .filter(Price.symbol == self.security.mnemonic)
            .orderby_desc(Price.date)
        )
        return query.all()

    def get_quantity(self) -> Decimal:
        """
        Returns the number of shares for the given security.
        It gets the number from all the accounts in the book.
        """
        from pydatum import Datum
        # Use today's date but reset hour and lower.
        today = Datum()
        today.today()
        today.end_of_day()
        return self.get_num_shares_on(today.value)

    def get_splits_query(self):
        """ Returns the query for all splits for this security """
        query = (
            self.book.session.query(Split)
            .join(Account)
            .filter(Account.type != AccountType.trading.value)
            .filter(Account.commodity_guid == self.security.guid)
        )
        return query

    def get_total_paid(self) -> Decimal:
        """ Returns the total amount paid, in currency, for the stocks owned """
        query = (
            self.get_splits_query()
        )
        splits = query.all()

        total = Decimal(0)
        for split in splits:
            total += split.value

        return total

    def get_total_paid_for_remaining_stock(self) -> Decimal:
        """ Returns the amount paid only for the remaining stock """
        paid = Decimal(0)

        accounts = self.get_holding_accounts()
        for acc in accounts:
            splits = self.get_available_splits_for_account(acc)
            paid += sum(split.value for split in splits)
        return paid

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

    #######################
    # Private
    # def get_income_in_account_period(self)

class SecuritiesAggregate(AggregateBase):
    """ Operates on security collections """
    # def __init__(self, book: Book):
    #     super(SecuritiesAggregate, self).__init__(book)

    def find(self, search_term: str) -> List[Commodity]:
        """ Searches for security by part of the name """
        query = (
            self.query
            .filter(Commodity.mnemonic.like('%' + search_term + '%') |
                    Commodity.fullname.like('%' + search_term + '%'))
        )
        return query.all()

    def get_all(self) -> List[Commodity]:
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
        assert security is not None
        assert isinstance(security, Commodity)

        return SecurityAggregate(self.book, security)

    def get_aggregate_for_symbol(self, symbol: str) -> SecurityAggregate:
        """ Returns the aggregate for the security found by full symbol """
        security = self.get_by_symbol(symbol)
        if not security:
            raise ValueError(f"Security not found in GC book: {symbol}!")
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
