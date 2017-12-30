#!/usr/bin/env python3
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid,
as well as income generated.
"""
import sys
#import os
import piecash
from datetime import datetime
#from piecash import Commodity, Price, Book
from piecash_utilities.report import report, execute_report
from gnucash_portfolio.lib import generic, templates, portfoliovalue


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

    stock_template = templates.load_jinja_template("stock_template.html")
    stock_rows = ""

    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        # get all commodities that are not currencies.
        all_stocks = portfoliovalue.get_all_stocks(book)
        for stock in all_stocks:
            for_date = datetime.today().date
            model = portfoliovalue.get_stock_model_from(book, stock, for_date)
            stock_rows += stock_template.render(model)

    # Load HTML template file.
    template = templates.load_jinja_template("template.html")
    # Render the full report.
    #return template.format(**locals())
    result = template.render(**locals())
    return result


####################################################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute_report(generate_report, book_url=sys.argv[1])
    else:
        book_url = generic.read_book_uri_from_console()
        generic.run_report_from_console("report_portfolio_value.html", lambda: generate_report(book_url))
