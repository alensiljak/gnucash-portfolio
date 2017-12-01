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
from gnucash_portfolio.lib import generic, templates

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

    model = {
        "test": None
    }
    model.test = "blah"
    
    # load display template
    template = templates.load_jinja_template("report_asset_allocation.html")
    # render template
    result = template.render(model=model)
    #**locals()

    return result

###################################################
if __name__ == "__main__":
    """
    Invoked from the command line.
    """
    if len(sys.argv) > 1:
        execute_report(generate_report, book_url=sys.argv[1])
    else:
        book_url = generic.read_book_uri_from_console()
        generic.run_report_from_console("report_asset_allocation.html", lambda: generate_asset_allocation_report(book_url))
