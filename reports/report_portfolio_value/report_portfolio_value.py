#!/usr/bin/env python3
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
#import pathlib
import piecash
from sqlalchemy import desc
from piecash import Commodity, Price
from piecash_utilities.report import report, execute_report
#CommodityOption, CommodityListOption
import gnucash_portfolio
from gnucash_portfolio.lib import generic, templates

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
    # Report variables
    shares_no = None
    avg_price = None

    # Load HTML template file.
    template = templates.load_jinja_template("template.html")
    stock_template = templates.load_jinja_template("stock_template.html")
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

def generate_stock_output(commodity: Commodity, template):
    """
    Generates statistics per symbol
    """
    #security = book.get(Commodity, mnemonic=symbol)
    exchange = commodity.namespace
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

    # Gain/loss percentage
    gain_loss_perc = 0
    if cost:
        gain_loss_perc = abs(gain_loss) * 100 / cost
        if gain_loss < 0:
            gain_loss_perc *= -1

    #base_currency = commodity.base_currency
    #return template.format(**locals())
    return template.render(**locals())

####################################################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute_report(generate_report, book_url=sys.argv[1])
    else:
        book_url = generic.read_book_uri_from_console()
        generic.run_report_from_console("report_portfolio_value.html", lambda: generate_report(book_url))
