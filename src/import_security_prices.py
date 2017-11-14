"""
Imports security prices into GnuCash file.
Usage:
import_security_prices.py <pricefile>.csv
"""
import sys

def import_file(filename):
    print(filename)
    return

###############################################################################
if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("You must send the file name as the first argument.")
    else:
        filename = sys.argv[1]
        import_file(filename)
    