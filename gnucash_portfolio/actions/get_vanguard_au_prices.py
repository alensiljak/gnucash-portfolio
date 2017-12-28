#!/usr/bin/python3
"""
The script downloads fund prices from Vanguard Australia site.
Retail Funds
Vanguard Diversified Bond Index Fund                  VAN0101AU   8123
Vanguard International Shares Index Fund (Hedged)     VAN0107AU   8146
Vanguard Australian Property Securities Index Fund    VAN0012AU   8147
Vanguard Australian Shares High Yield Fund            VAN0017AU   8148
"""
try: import simplejson as json 
except ImportError: import json
import requests

def __get_json_prices():
    """
    Downloads the latest prices in JSON.
    """
    url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPriceList.jsonp?1511191845895"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error"

    content = json.loads(response.content)
    return content

def __fetch_json_prices(user_funds):
    """
    This example loads the prices JSON. There are no retail funds there, however.
    """
    prices_json = __get_json_prices()

    for line in prices_json:
        port_id = line["portId"]
        if port_id not in user_funds:
            continue

        price_array = line["navPriceArray"]
        first_price = price_array[0]
        price_date = first_price["asOfDate"]
        price = first_price["price"]

        print(port_id, price_date, price)

def __load_fund_data():
    """
    Fetches retail fund prices.
    """
    #from .lib.generic import get_today

    #todaysdate =
    # TODO do we have a cached version?
    #tempdir = tempfile.gettempdir()
    #cache_file = os.path.join(tempdir, get_today())
    #cache =

    #url = "https://www.vanguardinvestments.com.au/retail/ret/investments/product.html"
    #url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPrice?portId=" + fund_id
    # pylint: disable=C0301
    url = "https://intlgra-globm-209.gra.international.vgdynamic.info/rs/gre/gra/datasets/auw-retail-listview-data.jsonp"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error"

    content = response.content
    content = str(content, 'utf-8')

    # clean-up the response
    if content.startswith("callback("):
        length = len(content) - 1
        content = content[9:length]

    # TODO cache the downloaded page.

    content_json = json.loads(content)
    return content_json["fundData"]

def __get_fund_price(fund_data, fund_id):
    """
    Returns the Price object with name, identifier, date, value, mstar_id.
    """
    from gnucash_portfolio.lib import messenger

    fund_info = fund_data[fund_id]

    price = messenger.Messenger(
        name=fund_info["name"],
        identifier=fund_info["identifier"],
        date=fund_info["asOfDate"],
        value=fund_info["navPrice"],
        mstar_id=fund_info["mStarID"]
    )
    # name
    # print(fund_info["identifier"],
    #       fund_info["navPrice"],
    #       fund_info["asOfDate"],
    #       fund_info["mStarID"],
    #       fund_info["name"])
    return price

def download_fund_prices(user_funds):
    """
    displays the prices
    """
    prices = []

    fund_data = __load_fund_data()
    for fund_id in user_funds:
        price = __get_fund_price(fund_data, fund_id)
        #print(price.identifier, price.date)
        prices.append(price)

    return prices

def test(user_funds):
    """ test method for console """
    prices = download_fund_prices(user_funds)
    for price in prices:
        print(price.identifier, price.date, price.value, price.name)

###########################################################
if __name__ == "__main__":
    USER_FUNDS = ["8123", "8146", "8148", "8147"]
    test(USER_FUNDS)
