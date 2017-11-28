#!/usr/bin/env python3
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
import piecash
from sqlalchemy import desc
from piecash import Commodity, Price
from piecash_utilities.report import report, execute_report
#CommodityOption, CommodityListOption
import gnucash_portfolio

####################################################################
@report(
    title="Portfolio Value",
    name="portfolio-value",
    menu_tip="Portfolio securities details",
    options_default_section="general",
)
def generate_report(book_url):
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
                    #):
    """
    Generates an HTML report content.
    """
    # TODO replace this with the received parameter / list?
    #symbol = "VTIP"

    # Report variables
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
    #return template.format(**locals())
    result = template.render(**locals())
    return result

def generate_stock_output(commodity, template):
    """
    Generates statistics per symbol
    """
    #security = book.get(Commodity, mnemonic=symbol)
    symbol = commodity.mnemonic

    shares_no = gnucash_portfolio.get_number_of_shares(commodity)
    #shares_no_disp = "{:,.2f}".format(shares_no)

    avg_price = gnucash_portfolio.get_avg_price(commodity)
    #avg_price_disp = "{:,.4f}".format(avg_price)

    # Last price
    last_price = commodity.prices.order_by(desc(Price.date)).first()
    price = None
    if last_price is not None:
        price = last_price.value
    #print("last price", last_price.value, last_price.currency.mnemonic)

    # Cost
    cost = shares_no * avg_price

    # Balance
    balance = 0
    if shares_no and price:
        balance = shares_no * price

    # Gain/Loss
    gain_loss = balance - cost

    #base_currency = commodity.base_currency
    #return template.format(**locals())
    return template.render(**locals())

def load_html_template(file_name):
    """
    Loads the jinja2 HTML template from the given file. 
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(script_path, file_name)
    # with open(file_path, 'r') as template_file:
    #     return template_file.read()
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(script_path))
    template = env.get_template(file_name)

    return template

####################################################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute_report(generate_report, book_url=sys.argv[1])
    else:
        print("The report uses a read-only access to the book.")
        print("book_url parameter expected as the first argument.")

        cfg = gnucash_portfolio.lib.settings.Settings()
        db_path_uri = cfg.database_uri
        result = generate_report(db_path_uri)

        # Save results.
        f = open("results.html", 'w')
        f.write(result)
        f.close()
        print("results saved in results.html file.")
