#!/usr/bin/env python3
"""
Asset Allocation report.
Asset Allocation is stored in the accompanying .json file and needs to be updated manually.
TODO:
    - ensure no duplicate symbols in different asset classes
    - convert the stock value to the base currency
    - calculate sum of allocations and compare to the set allocation value per group.
"""
import sys
from piecash_utilities.report import report, execute_report
from gnucash_portfolio.lib import generic, templates, database
from gnucash_portfolio.lib.assetallocation import AssetGroup, AssetClass, Stock, load_asset_allocation_model

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
    The otput is generated here. Separated from the generate_report function to allow executing
    from the command line.
    """
    model = load_asset_allocation_model(book_url)

    # load display template
    template = templates.load_jinja_template("report_asset_allocation.html")
    # render template
    result = template.render(model=model)
    # **locals()

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
        generic.run_report_from_console(
            "report_asset_allocation.html", lambda: generate_asset_allocation_report(book_url))
