"""
Provides access to the settings file.
"""
import json
from pprint import pprint

filename = "settings.json"
data = json.load(open(filename))

#class Settings:
def show_settings():
    """Displays the contents of the settings file"""
    data = load_settings()
    pprint(data)

def load_settings():
    """Returns the settings JSON from the file"""
    return data

def get_rates():
    """Returns the list of exchange rates from the settings"""
    data = load_settings()
    return data["exchangeRates"]

def get_currencies():
    """Fetches the list of currencies from the settings."""
    data = load_settings()
    return data["currencies"]

# If run directly, just display the settings file.
if __name__ == "__main__":
    #import sys
    show_settings()
