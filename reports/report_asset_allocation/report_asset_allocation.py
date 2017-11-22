#!/usr/bin/env python3
"""
Asset Allocation report.
Asset Allocation is stored in the accompanying .json file and needs to be updated manually.
"""
import os
import sys
import piecash
from piecash_utilities.report import report, execute_report
#import piecash_utilities
#from gnucash_portfolio import load_fund_data

@report(
    title="Asset Allocation",
    name="asset-allocation",
    menu_tip="Asset Allocation report",
    options_default_section="general",
)
def generate_report(book_url):
    """
    Generates the HTML report output.
    """
    return generate_asset_allocation_report(book_url)

def generate_asset_allocation_report(book_url):
    """
    The otput is generated here. Separeted from the generate_report function to allow executing
    from the command line.
    """
    # TODO read security information from the book.
    # TODO read asset allocation file
    # TODO calculate allocation in the book.

    return "YO!"

###################################################
if __name__ == "__main__":
    """
    Invoked from the command line.
    """
    # TODO Get the test book url.
    book_url = None
    result = generate_asset_allocation_report(book_url)
    print(result)
    #execute_report(generate_report, sys.argv[1])
    load_fund_data()
