#!/usr/bin/env python3
"""
Asset Allocation report.
Asset Allocation is stored in the accompanying .json file and needs to be updated manually.
"""
import sys
import json
from piecash_utilities.report import report, execute_report
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
    The otput is generated here. Separated from the generate_report function to allow executing
    from the command line.
    """
    # TODO load security information from the book.

    # read asset allocation file
    root_node = load_asset_allocation_file()
    aa = __parse_node(root_node)

    # TODO calculate allocation in the book.
    # TODO add all the stock values.

    model = {}
    model['test'] = "blah"
    model["allocation"] = aa

    # load display template
    template = templates.load_jinja_template("report_asset_allocation.html")
    # render template
    result = template.render(model=model)
    # **locals()

    return result


def __parse_node(node):
    """Creates an appropriate entity for the node. Recursive."""
    entity = None

    if "classes" in node:
        entity = AssetGroup(node)
        # Process child nodes
        for child_node in node["classes"]:
            child = __parse_node(child_node)
            #allocation_sum +=
            entity.classes.append(child)

    if "stocks" in node:
        # This is an Asset Class
        entity = AssetClass(node)

    return entity


def load_asset_allocation_file():
    """
    Loads asset allocation from the file.
    Returns the list of asset classes.
    """
    with open("assetAllocation.json", 'r') as json_file:
        allocation_json = json.load(json_file)

    return allocation_json


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
