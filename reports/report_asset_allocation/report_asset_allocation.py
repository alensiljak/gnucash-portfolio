#!/usr/bin/env python3
"""
Asset Allocation report.
Asset Allocation is stored in the accompanying .json file and needs to be updated manually.
"""
import os
import sys
import json
import piecash
from piecash_utilities.report import report, execute_report
#import piecash_utilities
from gnucash_portfolio.lib import generic, templates
from assetallocation import AssetAllocation, AssetGroup, AssetClass, Stock

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
    # TODO load security information from the book.

    # read asset allocation file
    classes = load_asset_allocation_file()
    aa = hydrate_asset_allocation(classes)

    # TODO calculate allocation in the book.

    model = {}
    model['test'] = "blah"
    model["allocation"] = aa

    # load display template
    template = templates.load_jinja_template("report_asset_allocation.html")
    # render template
    result = template.render(model=model)
    #**locals()

    return result

def hydrate_asset_allocation(classes) -> AssetAllocation:
    """When the allocation is loaded from a file, populate the Asset Allocation object"""
    aa = AssetAllocation()
    # Children can only be other classes.
    for asset_class in classes:
        __hydrate_node(aa, asset_class)

    return aa

def __hydrate_node(parent, node):
    """Populates the current node in the tree"""
    if "classes" in node:
        # This is a group
        item = AssetGroup(node)
        parent.classes.append(node)

        # Process child nodes
        for child_class in node["classes"]:
            __hydrate_node(item, child_class)

    if "stocks" in node:
        # This is an Asset Class
        item = AssetClass(node)

        for symbol in node["stocks"]:
            stock = Stock(symbol)
            item.stocks.append(stock)

    return node

def load_asset_allocation_file() -> []:
    """
    Loads asset allocation from the file.
    Returns the list of asset classes.
    """
    with open("assetAllocation.json", 'r') as json_file:
        classes = json.load(json_file)

    return classes

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
