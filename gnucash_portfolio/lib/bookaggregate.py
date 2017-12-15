"""
Aggregate for GnuCash book.
"""
import locale
import sys
import winreg
from piecash import Book

class BookAggregate:
    """ Encapsulates operations with GnuCash book """
    def __init__(self):
        """ constructor """
        self.book = Book()

    def query(self):
        """ DAL query """
        return self.book.session.query


    def get_default_currency(self):
        """ returns the book default currency """
        try:
            return self.book["default-currency"].value
        except KeyError:
            def_currency = self.__get_default_currency()


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
        custom_currency = self.__get_registry_key(key)
        def_curr = self.book["default-currency"] = self.__get_locale_currency()
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
