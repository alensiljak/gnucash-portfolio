""" Stocks aggregate object """
from datetime import date
from decimal import Decimal
from sqlalchemy import desc
from typing import List
from piecash import Account, Book, Commodity, Price, Split, Transaction
from gnucash_portfolio.accountaggregate import AccountAggregate, AccountsAggregate


class SecuritiesAggregate:
    """ Operates on security collections """
    def __init__(self, book: Book):
        self.book: Book = book

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
            self.book.session.query(Commodity)
            .filter(Commodity.namespace != "CURRENCY",
                    Commodity.mnemonic.in_(symbols))
        )
        return query.all()


class SecurityAggregate:
    """ Stocks aggregate """
    def __init__(self, book: Book, security: Commodity):
        self.book = book
        self.security = security

    def get_num_shares(self) -> Decimal:
        """
        Returns the number of shares for the given security.
        It gets the number from all the accounts in the book.
        """
        today = date.today
        return self.get_num_shares_on(today)


    def get_num_shares_on(self, on_date: date) -> Decimal:
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
