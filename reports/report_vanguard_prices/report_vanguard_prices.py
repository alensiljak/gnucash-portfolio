"""
Displays latest prices for Vanguard Australia retail funds.
The fund codes should be specified as report parameters.
"""
import sys
import os
from piecash_utilities.report import report, execute_report, StringOption
import jinja2
from gnucash_portfolio import get_vanguard_au_prices
from gnucash_portfolio.lib import generic

@report(
    title="Vanguard Prices",
    name="latest-vanguard-prices",
    menu_tip="Latest retail fund prices from Vanguard Australia",
    options_default_section="general",
)
def generate_report(
        book_url,
        fund_ids: StringOption(
            section="Funds",
            sort_tag="c",
            documentation_string="Comma-separated list of fund ids.",
            default_value="8123,8146,8148,8147")
    ):
    """Generates the report output"""
    return render_report(book_url, fund_ids)

def render_report(book_url, fund_ids):
    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, '.'))
    template = env.get_template("template.html")

    #user_funds = ["8123", "8146", "8148", "8147"]
    user_funds = fund_ids.strip().split(",")
    #print(user_funds)
    prices = get_vanguard_au_prices.download_fund_prices(user_funds)

    return template.render(
            enumerate=enumerate,
            list=list,
            path_report=os.path.abspath(__file__),
            **vars()
        )

def test():
    """Runs the report from the console."""
    # TODO get the fund list as parameter(s)
    user_funds = ["8123", "8146", "8148", "8147"]
    prices = get_vanguard_au_prices.download_fund_prices(user_funds)

####################################################################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute_report(generate_report, book_url=sys.argv[1])
    else:
        #print("book_url parameter expected")
        # We don't care about the book here as the data is not touched.
        #test()
        book_url = generic.read_book_uri_from_console()
        #options.default_value="8123,8146,8148,8147"
        generic.run_report_from_console(
            output_file_name="report_vanguard_prices.html", 
            callback=lambda: render_report(book_url, "8123,8146,8148,8147")
        )
