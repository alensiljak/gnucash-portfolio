""" Currencies service """

from logging import log, INFO
import locale
import sys
from decimal import Decimal
from enum import Enum, auto
from typing import List
from sqlalchemy import desc
from piecash import Book, Commodity, Price
from pricedb import PriceModel


class CommodityTypes(Enum):
    """ Commodity namespaces """
    CURRENCY = auto()


class CurrencyAggregate:
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
        """ Returns the latest rate compared to default currency """
        default_currency = self.book.default_currency
        # Ensure that the rate is against the default currency only.
        query = (
            self.currency.prices
                .filter(Price.currency == default_currency)
                .order_by(desc(Price.date))
        )
        latest_price = query.first()
        return latest_price


class CurrenciesAggregate:
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

    def get_amount_in_base_currency(self, currency: str, amount: Decimal) -> Decimal:
        """ Calculates the amount in base currency """
        assert isinstance(amount, Decimal)

        # If this is already the base currency, do nothing.
        if currency == self.get_default_currency().mnemonic:
            return amount

        agg = self.get_currency_aggregate_by_symbol(currency)
        if not agg:
            raise ValueError(f"Currency not found: {currency}!")

        # TODO use pricedb for the price.
        rate_to_base = agg.get_latest_price()
        if not rate_to_base:
            raise ValueError(f"Latest price not found for {currency}!")
        assert isinstance(rate_to_base.value, Decimal)

        result = amount * rate_to_base.value
        return result

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

    def get_currency_aggregate_by_symbol(self, symbol: str) -> CurrencyAggregate:
        """ Creates currency aggregate for the given currency symbol """
        currency = self.get_by_symbol(symbol)
        result = self.get_currency_aggregate(currency)
        return result

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
            # exists_query = exists(rates_query)
            has_rate = currency.prices.filter(Price.date == rate.datetime.date()).first()
            # has_rate = (
            #     self.book.session.query(Price)
            #     .filter(Price.date == rate.date.date())
            #     .filter(Price.currency == currency)
            # )
            if not has_rate:
                log(INFO, "Creating entry for %s, %s, %s, %s",
                    base_currency.mnemonic, currency.mnemonic, rate.datetime.date(), amount)
                # Save the price in the exchange currency, not the default.
                # Invert the rate in that case.
                inverted_rate = 1 / amount
                inverted_rate = inverted_rate.quantize(Decimal('.00000000'))

                price = Price(commodity=currency,
                              currency=base_currency,
                              date=rate.datetime.date(),
                              value=str(inverted_rate))
                have_new_rates = True

        # Save the book after the prices have been created.
        if have_new_rates:
            log(INFO, "Saving new prices...")
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
        """ Read currency from windows registry """
        import winreg

        root = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r'SOFTWARE\GSettings\org\gnucash\general', 0, winreg.KEY_READ)
        [pathname, regtype] = (winreg.QueryValueEx(root, key))
        winreg.CloseKey(root)
        return pathname

    def __get_locale_currency(self):
        if locale.getlocale() == (None, None):
            locale.setlocale(locale.LC_ALL, '')
        mnemonic = locale.localeconv()['int_curr_symbol'].strip() or "EUR"
        return self.book.currencies(mnemonic=mnemonic)
