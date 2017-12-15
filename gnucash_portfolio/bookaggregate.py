"""
Aggregate for GnuCash book.
"""
import locale
import sys
import winreg
from typing import List
from piecash import Book, Commodity
from gnucash_portfolio.lib.currencies import CurrencyAggregate
from gnucash_portfolio.lib.database import Database


class BookAggregate:
    """ Encapsulates operations with GnuCash book """
    def __init__(self):
        """ constructor """
        self.book: Book = None
        self.default_currency = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.book:
            return

        self.book.close()


    @property
    def session(self):
        """ Access to sql session """
        return self.book.session

    def get_currencies(self):
        """ Returns the currencies used in the book """
        return self.get_currencies_query().all()

    def get_currencies_query(self):
        """ returns the query only """
        return self.book.session.query(Commodity).filter_by(namespace="CURRENCY")


    def get_currency_symbols(self) -> List[str]:
        """ Returns the used currencies' symbols as an array """
        result = []
        for cur in self.get_currencies():
            result.append(cur.mnemonic)
        return result

    def get_default_currency(self) -> Commodity:
        """ returns the book default currency """
        if self.default_currency:
            return self.default_currency
        else:
            def_currency = self.__get_default_currency()
            self.default_currency = def_currency
            return def_currency


    def get_currency_aggregate(self, currency: Commodity):
        """ Creates a currency aggregate for the given currency """
        result = CurrencyAggregate(currency)
        return result

    def __get_default_currency(self):
        """Read the default currency from GnuCash preferences"""
        # If we are on Windows, read from registry.
        if sys.platform == "win32":
            # read from registry
            def_curr = self.book["default-currency"] = self.__get_default_currency_windows()
        else:
            # return the currency from locale.
            # todo: Read the preferences on other operating systems.
            def_curr = self.book["default-currency"] = self.__get_locale_currency()

        return def_curr

    def __get_default_currency_windows(self):
        key = "currency-choice-locale"
        locale_selected = self.__get_registry_key(key)
        if locale_selected:
            return self.__get_locale_currency()

        key = "currency-choice-other"
        custom_selected = self.__get_registry_key(key)
        if not custom_selected:
            # This is an invalid state
            return None

        key = "currency-other"
        custom_symbol = self.__get_registry_key(key)
        # self.default_currency =
        def_curr = self.get_book().currencies(mnemonic=custom_symbol)
        return def_curr

    def __get_registry_key(self, key):
        root = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r'SOFTWARE\GSettings\org\gnucash\general', 0, winreg.KEY_READ)
        [Pathname, regtype] = (winreg.QueryValueEx(root, key))
        #print(key, [Pathname, regtype])
        winreg.CloseKey(root)
        return Pathname

    def __get_locale_currency(self):
        if locale.getlocale() == (None, None):
            locale.setlocale(locale.LC_ALL, '')
        mnemonic = locale.localeconv()['int_curr_symbol'].strip() or "EUR"
        return self.book.currencies(mnemonic=mnemonic)

    def get_book(self):
        """ Returns an open GnuCash book. Intended for internal use. """
        if not self.book:
            self.book = Database().open_book()

        return self.book
