#!/usr/bin/env python3
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
import piecash
from piecash import Commodity
from piecash_utilities.report import report, execute_report
#CommodityOption, CommodityListOption
#import symbol_balance
from decimal import Decimal

####################################################################
@report(
    title="Security Analysis",
    name="security-analysis-report",
    menu_tip="Security details",
    options_default_section="general",
)
def generate_report(book_url
                    # commodity: CommodityOption(
                    #     section="Commodity",
                    #     sort_tag="a",
                    #     documentation_string="This is a stock",
                    #     default_value="VTIP"),
                    # commodity_list: CommodityListOption(
                    #     section="Commodity",
                    #     sort_tag="a",
                    #     documentation_string="This is a stock",
                    #     default_value="VTIP")
                    ):
    """
    Generates an HTML report content.
    """
    # TODO replace this with the received parameter / list.
    #symbol = "VTIP"
    shares_no = None
    avg_price = None

    # Load HTML template file.
    template = load_html_template("template.html")
    stock_template = load_html_template("stock_template.html")
    stock_rows = ""

    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        # get all commodities that are not currencies.
        all_stocks = book.session.query(Commodity).filter(Commodity.namespace != "CURRENCY",
                                                          Commodity.mnemonic != "template").order_by(Commodity.mnemonic).all()
        for stock in all_stocks:
            #print("Found", c.mnemonic)
            stock_rows += generate_stock_output(stock, stock_template)

    # Render the full report.
    return template.format(**locals())

def generate_stock_output(commodity, template):
    """
    Generates statistics per symbol
    """
    #security = book.get(Commodity, mnemonic=symbol)
    symbol = commodity.mnemonic
    
    shares_no = get_number_of_shares(commodity)
    shares_no = "{:,.2f}".format(shares_no)

    avg_price = get_avg_price(commodity)
    avg_price = "{:,.4f}".format(avg_price)

    #base_currency = commodity.base_currency

    return template.format(**locals())

def load_html_template(file_name):
    """
    Loads the template from a file. This makes it easier to edit the template in an editor.
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_path, file_name)

    with open(file_path, 'r') as template_file:
        return template_file.read()

def get_avg_price(security):
    """
    Calculates the average price paid for the security.
    security = Commodity
    Returns Decimal value.
    """
    #print("Calculating stats for", security.mnemonic)
    avg_price = Decimal(0)

    #return sum([sp.quantity for sp in self.splits]) * self.sign

    price_total = Decimal(0)
    price_count = 0

    for account in security.accounts:
        # Ignore trading accounts.
        if account.type == "TRADING":
            continue

        for split in account.splits:
            price = split.value / split.quantity
            #print(price)
            price_count += 1
            price_total += price

    #print(price_total, price_count)
    if price_count:
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
