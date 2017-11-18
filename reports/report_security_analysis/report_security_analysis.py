#!/usr/bin/env python
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
import piecash
from piecash import Commodity
from piecash_utilities.report import report, execute_report
import symbol_balance

####################################################################
@report(
    title="Security Analysis",
    name="security-analysis-report",
    menu_tip="Security details",
    options_default_section="general",
)
def generate_report(book_url):
    """
    Generates an HTML report content.
    """
    symbol = "VTIP"
    shares_no = None
    avg_price = None

    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        security = book.get(Commodity, mnemonic=symbol)
        shares_no = symbol_balance.get_number_of_shares(security)
        avg_price = symbol_balance.get_avg_price(security)

    # Load HTML template file.
    template = load_html_template()
    return template.format(**locals())

def load_html_template():
    """
    Loads the template from a file. This makes it easier to edit the template in an editor.
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    template_file_name = "template.html"
    file_path = os.path.join(script_path, template_file_name)

    with open(file_path, 'r') as template_file:
        return template_file.read()

####################################################################
if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
