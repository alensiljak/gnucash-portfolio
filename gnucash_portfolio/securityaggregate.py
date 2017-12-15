""" Stocks aggregate object """
from decimal import Decimal
from sqlalchemy import desc
from piecash import Book, Commodity, Price

class SecurityAggregate:
    """ Stocks aggregate """
    def __init__(self, book: Book):
        self.book = book

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

    def get_number_of_shares(self, security: Commodity) -> Decimal:
        """
        Returns the number of shares for the given security.
        It gets the number from all the accounts in the book.
        """
        total_quantity = Decimal(0)
        #total_balance = Decimal(0)

        for account in security.accounts:
            # exclude Trading accouns explicitly.
            if account.type == "TRADING":
                continue

            quantity = account.get_balance()

            total_quantity += quantity

        return total_quantity

    def get_last_available_price(self, security: Commodity) -> Price:
        """ Finds the last available price for security """
        last_price = security.prices.order_by(desc(Price.date)).first()
        #return last_price.value
        return last_price

    def get_avg_price(self, security: Commodity) -> Decimal:
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

        for account in security.accounts:
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