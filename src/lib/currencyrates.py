"""
Fetches the current exchange rates.
Currently uses Fixer API.

To-Do:
- download only the requested rates

"""
#import os
import glob
import json
from fixerio import Fixerio
import settings
import time

# if run from editor:
#settings_path = "settings.json"
# if run from command-line:
settings_path = "../settings.json"

class CurrencyRatesRetriever:
    """Retrieves prices from data files or online provider(s)"""

    __settings = None

    def __init__(self):
        __settings = settings.Settings(settings_path)
        return

    def get_latest_rates(self):
        """Returns the latest rates. Reads from the file and downloads the latest
        rates if the file is not current."""

        # find the current date
        today = time.strftime("%Y-%m-%d")
        print("Today's date: " + today)

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
        latestRates = self.__download_rates(base_currency)
        print(latestRates)

        # todo: get only the requested rates
        print(latestRates["rates"])

        # todo: save to file
        #rates = json.loads(latestJson)
        #print(rates)

    def __download_rates(self, base_currency):
        """Downloads the latest rates using Fixerio. Returns json."""
        fxrio = Fixerio(base=base_currency)
        return fxrio.latest()

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
    runner = CurrencyRatesRetriever()
    runner.display_rates()
