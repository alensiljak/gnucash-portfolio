""" Aggregate for GnuCash book. """
from typing import List
from piecash import Account, Book, Commodity
from gnucash_portfolio.lib.database import Database, Settings
from gnucash_portfolio.currencyaggregate import CurrenciesAggregate
from gnucash_portfolio.pricesaggregate import PricesAggregate
from gnucash_portfolio.accountaggregate import AccountsAggregate, AccountType
from gnucash_portfolio.assetallocation import AssetAllocationAggregate
from gnucash_portfolio.scheduledtxaggregate import ScheduledTxsAggregate
from gnucash_portfolio.securitiesaggregate import SecuritiesAggregate


class BookAggregate:
    """ Encapsulates operations with GnuCash book """

    def __init__(self, settings: Settings = None,
                 for_writing=False):
        """
        Accepts custom settings object. Useful for testing.
        """
        self.__book: Book = None
        self.__for_writing = for_writing

        # Aggregates
        self.__currencies_aggregate: CurrenciesAggregate = None
        self.__accounts_aggregate: AccountsAggregate = None
        self.__prices_aggregate: PricesAggregate = None
        self.__scheduled_tx_aggregate: ScheduledTxsAggregate = None
        self.__securities_aggregate: SecuritiesAggregate = None

        self.__settings: Settings = None

        if settings:
            self.__settings = settings

    def __enter__(self):
        #self.book = Database().open_book()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__book:
            self.__book.close()

    @property
    def book(self):
        """ GnuCash Book. Opens the book or creates an in-memory database, based on settings. """
        if not self.__book:
            # Create/open the book.
            book_uri = self.settings.database_path
            self.__book = Database(book_uri).open_book(
                for_writing=self.__for_writing)

        return self.__book

    @book.setter
    def book(self, value):
        """ setter for book """
        self.__book = value

    @property
    def session(self):
        """ Access to sql session """
        return self.book.session

    @property
    def settings(self):
        """ Settings """
        if not self.__settings:
            self.__settings: Settings = Settings()

        return self.__settings

    @property
    def accounts(self) -> AccountsAggregate:
        """ Returns the Accounts aggregate """
        if not self.__accounts_aggregate:
            self.__accounts_aggregate = AccountsAggregate(self.book)
        return self.__accounts_aggregate

    @property
    def currencies(self) -> CurrenciesAggregate:
        """ Returns the Currencies aggregate """
        if not self.__currencies_aggregate:
            self.__currencies_aggregate = CurrenciesAggregate(self.book)
        return self.__currencies_aggregate

    @property
    def prices(self):
        """ Prices aggregate """
        if not self.__prices_aggregate:
            self.__prices_aggregate = PricesAggregate(self.book)
        return self.__prices_aggregate

    @property
    def scheduled(self) -> ScheduledTxsAggregate:
        """ Scheduled Transactions """
        if not self.__scheduled_tx_aggregate:
            self.__scheduled_tx_aggregate = ScheduledTxsAggregate(self.book)
        return self.__scheduled_tx_aggregate

    @property
    def securities(self):
        """ Returns securities aggregate """
        if not self.__securities_aggregate:
            self.__securities_aggregate = SecuritiesAggregate(self.book)
        return self.__securities_aggregate

    def save(self):
        """ Save all changes """
        self.book.flush()
        self.book.save()

    def get_currency_symbols(self) -> List[str]:
        """ Returns the used currencies' symbols as an array """
        result = []
        currencies = self.currencies.get_book_currencies()
        for cur in currencies:
            result.append(cur.mnemonic)
        return result

    def get_asset_allocation(self) -> AssetAllocationAggregate:
        """ Creates an Asset Allocation aggregate """
        return AssetAllocationAggregate(self.book)
