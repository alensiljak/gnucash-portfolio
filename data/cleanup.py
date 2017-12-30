""" Delete all .log files in the (current) directory """
#import sys
import os

dir_name = "./"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".log"):
        os.remove(os.path.join(dir_name, item))
