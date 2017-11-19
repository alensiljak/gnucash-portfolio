#!/usr/bin/env python3
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
import piecash
from piecash import Commodity
from piecash_utilities.report import report, execute_report, CommodityOption, CommodityListOption
#import symbol_balance
from decimal import Decimal

####################################################################
@report(
    title="Security Analysis",
    name="security-analysis-report",
    menu_tip="Security details",
    options_default_section="general",
)
def generate_report(book_url,
                    commodity: CommodityOption(
                        section="Commodity",
                        sort_tag="a",
                        documentation_string="This is a stock",
                        default_value="VTIP"),
                    commodity_list: CommodityListOption(
                        section="Commodity",
                        sort_tag="a",
                        documentation_string="This is a stock",
                        default_value="VTIP")
                    ):
    """
    Generates an HTML report content.
    """
    print("Symbol requested:", commodity)
    #print(commodity.name)
    print(commodity_list)

    # TODO replace this with the received parameter / list.
    symbol = "VTIP"
    shares_no = None
    avg_price = None

    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        security = book.get(Commodity, mnemonic=symbol)
        shares_no = get_number_of_shares(security)
        avg_price = get_avg_price(security)

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

def get_avg_price(security):
    """
    Calculates the average price paid for the security.
    security = Commodity
    """
    avg_price = Decimal(0)

    #return sum([sp.quantity for sp in self.splits]) * self.sign

    for account in security.accounts:
        # Ignore trading accounts.
        if account.type == "TRADING":
            continue

        price_total = Decimal(0)
        price_count = 0

        for split in account.splits:
            price = split.value / split.quantity
            #print(price)
            price_count += 1
            price_total += price

    avg_price = price_total / price_count
    return avg_price

def get_number_of_shares(security):
    """
    Returns the number of shares for the given security.
    It gets the number from all the accounts in the book.
    """
    total_quantity = Decimal(0)
    #total_balance = Decimal(0)

    for account in security.accounts:
        # exclude Trading accouns explicitly.
        if account.type == "TRADING":
            continue

        balance = account.get_balance()
        quantity = account.get_quantity()

        #print(account.fullname, quantity, balance)
        #total_balance += balance
        total_quantity += quantity

    #print("Balance:", total_balance)
    return total_quantity

####################################################################
if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
