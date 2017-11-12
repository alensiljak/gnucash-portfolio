"""
Provides access to the settings file.
"""

import json
from pprint import pprint

filename = "settings.json"

def show_settings():
    """Displays the contents of the settings file"""

    data = json.load(open(filename))
    pprint(data)
