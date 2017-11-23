"""
Displays latest prices for Vanguard Australia retail funds.
The fund codes should be specified as report parameters.
"""
import sys
import os
from piecash_utilities.report import report, execute_report, StringOption
import jinja2
from gnucash_portfolio import get_vanguard_au_prices

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
    # with piecash.open_book ...
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

    #get_vanguard_au_prices.main(user_funds)
    #return "yo"

def main():
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
        main()