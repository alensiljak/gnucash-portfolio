"""
Copies the current report settings from gnucash directory into this one.
"""
import os
from os.path import expanduser
#from os import path
from datetime import datetime
from shutil import copyfile

def get_gnucash_dir():
    home = expanduser("~")
    return os.path.abspath(home + "/.gnucash/")

def get_reports_settings_path():
    filename = "saved-reports-2.4"
    return os.path.abspath(get_gnucash_dir() + "/" + filename)

source = get_reports_settings_path
destination = os.path.relpath("./")

# if os.path.exists(destination) and os.path.isfile(destination):
#     print("There is already a file in the current directory.")
#     # copy by appending a number (?)
#     append_date = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
#     destination = os.path.relpath("./" + filename + "." + append_date + ".bak")

# copy file
copyfile(source, destination)
print("File copied:", destination)
