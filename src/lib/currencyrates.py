"""
Fetches the current exchange rates.
Currently uses Fixer API.

To-Do:
- download only the requested rates

"""
#import os
import glob
from fixerio import Fixerio

def get_latest_rates():
    """Returns the latest rates. Reads from the file and downloads the latest
    rates if the file is not current."""
    # todo find the current date
    # todo get the latest downloaded rates file
    latest = __get_latest_downloaded_rates_date()
    if not latest:
        print("No files available")
    else:
        print("latest downloaded rates are from ")
        print(latest)

    return latest

def __get_latest_downloaded_rates_date():
    """Checks for the latest date of the downloaded rates"""
    # iterate over .json files in the data directory
    all_files = __get_all_currency_files()
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

def __get_all_currency_files():
    #file_path = os.path.relpath('../data/cur*.csv')
    #os.listdir(file_path)
    return glob.glob("../data/cur*.json")

def __download_rates():
    """Downloads the latest rates using Fixerio"""
    fxrio = Fixerio()
    return fxrio.latest()

def display_rates():
    """Display the latest rates"""
    latest = get_latest_rates()
    print(latest)
    return

# If run directly, download the latest rates if not found, and display the rates.
if __name__ == "__main__":
    # Display the latest rates
    #latest = download_rates()
    #latest = get_latest_rates()
    #output = __get_all_currency_files()
    display_rates()
