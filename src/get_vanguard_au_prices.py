#!/usr/bin/python3
"""
The script downloads fund prices from Vanguard Australia site.
Retail Funds
Vanguard Diversified Bond Index Fund                  VAN0101AU   8123
Vanguard Australian Property Securities Index Fund    VAN0012AU   8147
Vanguard Australian Shares High Yield Fund            VAN0017AU   8148
Vanguard International Shares Index Fund (Hedged)     VAN0107AU   8146
"""
import requests
import json

user_funds = ["8123", "8147", "8148", "8146"]

def get_json_prices():
    """
    Downloads the latest prices in JSON.
    """
    url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPriceList.jsonp?1511191845895"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error"

    content = json.loads(response.content)
    return content

def fetch_json_prices():
    """
    This example loads the prices JSON. There are no retail funds there, however.
    """
    prices_json = get_json_prices()

    for line in prices_json:
        port_id = line["portId"]
        if port_id not in user_funds:
            continue

        price_array = line["navPriceArray"]
        first_price = price_array[0]
        price_date = first_price["asOfDate"]
        price = first_price["price"]
        
        print(port_id, price_date, price)

def load_fund_data():
    """
    Fetches retail fund prices.
    """
    #url = "https://www.vanguardinvestments.com.au/retail/ret/investments/product.html"
    #url = "https://www.vanguardinvestments.com.au/retail/mvc/getNavPrice?portId=" + fund_id
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

    content_json = json.loads(content)
    return content_json["fundData"]

def get_fund_price(fund_data, fund_id):
    fund_info = fund_data[fund_id]

    # name
    print(fund_info["identifier"],
          fund_info["navPrice"],
          fund_info["asOfDate"],
          fund_info["mStarID"],
          fund_info["name"])

###########################################################
fund_data = load_fund_data()
for fund_id in user_funds:
    get_fund_price(fund_data, fund_id)
