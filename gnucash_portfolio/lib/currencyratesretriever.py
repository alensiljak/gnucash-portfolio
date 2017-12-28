#!/usr/bin/python3
"""
Fetches the current exchange rates.
Currently uses Fixer API.
"""
import glob
try: import simplejson as json
except ImportError: import json
import os
from logging import log, ERROR
from fixerio import Fixerio
from gnucash_portfolio.lib import generic
from gnucash_portfolio.lib.settings import Settings


class CurrencyRatesRetriever:
    """Retrieves prices from data files or online provider(s)"""

    settings = None
    cache_path = "data/"

    def __init__(self, settings):
        self.settings: Settings = settings #.Settings(settings_path)
        return

    def get_latest_rates(self):
        """
        Retrieves the latest rates. If cached, loads cached file, otherwise
        downloads the rates.
        """
        # todo: check cached rates
        if self.latest_rates_exist:
            # returned cached content
            return self.__read_rates_from_file()
        else:
            base = self.settings.base_currency
            symbols = self.settings.get_currencies()
            return self.__download_rates(base, symbols)

    def __download_rates(self, base_currency, symbols):
        """
        Downloads the latest rates. Requires base currency and a list of currencies to
        retrieve.
        """
        # get default currency
        if not base_currency:
            # use the base currency from the settings.
            base_currency = self.settings.base_currency
            log(ERROR, "Base currency not sent to currency rates retrieval. Using settings:",
                base_currency)

        print("Downloading rates...")

        # Downloads the latest rates using Fixerio. Returns dict.
        # https://pypi.python.org/pypi/fixerio
        fxrio = Fixerio(base=base_currency, symbols=symbols)
        latest_rates = fxrio.latest()

        # todo: since these are daily rates, cache them into a file
        self.__save_rates(latest_rates)

        return latest_rates

    def get_yesterdays_file_path(self):
        '''
        Full path to the today's rates file.
        '''
        #today = generic.get_today()
        yesterday = generic.get_date_iso_string(generic.get_yesterday())
        return self.__get_rate_file_path(yesterday)

    @property
    def latest_rates_exist(self):
        '''
        Check if latest rates cached file exists.
        '''
        file_path = self.get_yesterdays_file_path()
        #print("Checking for", file_path)
        exists = os.path.isfile(file_path)

        if exists:
            print("Cached file found for", file_path)

        return exists

    def __get_rate_file_path(self, filename):
        """
        Assemble full file path for the given name (date).
        """
        return os.path.relpath(self.cache_path + filename + ".json")

    def __read_rates_from_file(self):
        file_path = self.get_yesterdays_file_path()

        with open(file_path, 'r') as file:
            content = file.read()
            return json.loads(content)

    def __save_rates(self, rates):
        """
        Saves the retrieved rates into a cache file
        """
        file_date = rates["date"]
        filename = self.__get_rate_file_path(file_date)

        content = json.dumps(rates)

        with open(filename, 'w') as file:
            file.write(content)

    def __x_get_latest_rates(self):
        """
        Returns the latest rates. Reads from the file and downloads the latest
        rates if the file is not current.
        """

        # todo get the latest downloaded rates file
        latest = self.__get_latest_downloaded_rates_date()
        if not latest:
            # Download from the net.
            print("No currency rate files available in data directory.")
            self.__download_and_save_rates()

        # todo open the file and display rates

        print("latest downloaded rates are from ")
        print(latest)

        return latest

    def __get_latest_downloaded_rates_date(self):
        """Checks for the latest date of the downloaded rates"""
        # iterate over .json files in the data directory
        all_files = self.__get_all_currency_files()
        if not all_files:
            return

        print(all_files)
        # todo get the largest date, not the smallest!
        smallest = min(all_files)
        print(smallest)
        index = all_files.index(smallest)
        print(index)
        # todo get the latest one
        return

    def __get_all_currency_files(self):
        #file_path = os.path.relpath('../data/cur*.csv')
        #os.listdir(file_path)
        return glob.glob("../data/cur*.json")

    def __download_and_save_rates(self):
        """Downloads the latest rates and saves into a text file"""
        # todo: Get the base currency from gnucash file.
        base_currency = 'EUR'

        # todo: get the desired rates from the settings or gnucash file?
        rates_to_download = ["AUD"]

        # download rates
        latestRates = self.__download_rates(base_currency, rates_to_download)
        #print(latestRates)

        # todo: get only the requested rates
        print(latestRates["rates"])

        # todo: save to file
        #rates = json.loads(latestJson)
        #print(rates)

    def display_rates(self):
        """Display the latest rates"""
        latest = self.get_latest_rates()
        if latest:
            print(latest)
        return

# If run directly, download the latest rates if not found, and display the rates.
if __name__ == "__main__":
    # Display the latest rates
    #latest = download_rates()
    #latest = get_latest_rates()
    #output = __get_all_currency_files()
    runner = CurrencyRatesRetriever(None)
    runner.display_rates()
