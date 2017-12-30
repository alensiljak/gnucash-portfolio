""" Currencies service """

from logging import log, INFO
import locale
import sys
import winreg
from decimal import Decimal
from typing import List
from sqlalchemy import desc
#from sqlalchemy.sql.expression import exists
from piecash import Book, Commodity, Price
from gnucash_portfolio.model.price_model import PriceModel


class CurrencyAggregate():
    """ Service/aggregate for a single currency """
    def __init__(self, book: Book, currency: Commodity):
        """ constructor """
        self.book = book
        self.currency = currency

    def get_latest_rate(self, other: Commodity) -> Price:
        """ Fetches the latest available rate for the currency pair """
        query = (
            self.currency.prices
            .filter(Price.commodity == self.currency,
                    Price.currency == other)
            )
        return query.first()

    def get_latest_price(self) -> Price:
        """ Returns the latest price entity """
        query = (
            self.currency.prices
            .order_by(desc(Price.date))
        )
        latest_price = query.first()
        return latest_price


class CurrenciesAggregate():
    """ Service/aggregate for currencies """
    def __init__(self, book: Book):
        """ constructor """
        self.book = book
        self.default_currency: Commodity = None

    @property
    def currencies_query(self):
        """ returns the query only """
        return (
            self.book.session.query(Commodity)
            .filter_by(namespace="CURRENCY")
        )

    @property
    def currencies_query_sorted(self):
        """ currencies, sorted alphabetically """
        return self.currencies_query.order_by(Commodity.mnemonic)

    def get_default_currency(self) -> Commodity:
        """ returns the book default currency """
        result = None

        if self.default_currency:
            result = self.default_currency
        else:
            def_currency = self.__get_default_currency()
            self.default_currency = def_currency
            result = def_currency

        return result

    def get_book_currencies(self) -> List[Commodity]:
        """ Returns currencies used in the book """
        query = (
            self.currencies_query
            .order_by(Commodity.mnemonic)
        )
        return query.all()

    def get_currency_aggregate(self, cur: Commodity) -> CurrencyAggregate:
        """ Returns a single-currency aggregate """
        return CurrencyAggregate(self.book, cur)

    def get_by_symbol(self, symbol: str) -> Commodity:
        """ Loads currency by symbol """
        assert isinstance(symbol, str)

        query = (
            self.currencies_query
            .filter(Commodity.mnemonic == symbol)
        )
        return query.one()

    def import_fx_rates(self, rates: List[PriceModel]):
        """ Imports the given prices into database. Write operation! """
        have_new_rates = False

        base_currency = self.get_default_currency()

        for rate in rates:
            assert isinstance(rate, PriceModel)

            currency = self.get_by_symbol(rate.symbol)
            amount = rate.value

            # Do not import duplicate prices.
            # todo: if the price differs, update it!
            #exists_query = exists(rates_query)
            has_rate = currency.prices.filter(Price.date == rate.date).first()
            if not has_rate:
                log(INFO, "Creating entry for", base_currency.mnemonic, currency.mnemonic,
                    rate.date, amount)
                # Save the price in the exchange currency, not the default.
                # Invert the rate in that case.
                inverted_rate = 1 / amount
                inverted_rate = inverted_rate.quantize(Decimal('.00000000'))

                price = Price(commodity=currency,
                              currency=base_currency,
                              date=rate.date,
                              value=str(inverted_rate))
                have_new_rates = True

        # Save the book after the prices have been created.
        if have_new_rates:
            self.book.flush()
            self.book.save()
        else:
            log(INFO, "No prices imported.")

    ##############
    # Private

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
        def_curr = self.book.currencies(mnemonic=custom_symbol)
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
