"""
Copies the reports from this directory into .gnucash directory in the profile directory.
After this is performed, run `gc_report` the first time or if the parameters have changed.
"""
import os
#import shutil
import distutils
from distutils import dir_util
# from os.path import expanduser
from pathlib import Path
from os import path

# get all the report folders
report_folders = []
#subdirs = os.listdir(".")
#subdirs = os.walk(".")
subdirs = os.scandir(".")
for subdir in subdirs:
    if not subdir.is_dir():
        continue
    #print(subdir)
    report_folders.append(subdir)

# copy to the destination
#home = expanduser("~")
home = Path.home()
gnucash_dir = path.abspath(home + "/.gnucash/")

for report_dir in report_folders:
    report_name = report_dir.name
    dst = path.join(gnucash_dir, report_name)
    #shutil.copytree(report_name, dst)
    distutils.dir_util.copy_tree(report_name, dst)
    print("Copied", report_name)