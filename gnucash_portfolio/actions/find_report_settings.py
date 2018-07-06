"""
Opens windows explorer in the .gnucash settings directory, with the report customization
settings selected.
Useful for comparison of the report customization options with a backup file. If you want
to use the same settings on multiple computers, the file needs to be synchronized manually.
"""
import subprocess
from os import path

def get_gnucash_dir():
    # from os.path import expanduser
    # home = expanduser("~")
    from pathlib import Path
    home = Path.home()

    return path.abspath(home + "/.gnucash/")

def get_reports_settings_path():
    filename = "saved-reports-2.4"
    return path.abspath(get_gnucash_dir() + "/" + filename)

# This will open the target selected.
#subprocess.Popen(r'explorer /select,' + home)

destination = get_reports_settings_path()
subprocess.Popen(r'explorer /select,' + destination)
