"""
        Deprecated?
"""
from typing import List


def download_fund_prices(user_funds) -> List[str]:
    """
    downloads, parses, and returns the price list
    """
    prices = []
    #agent = VanguardAuDownloader()

    # for symbol in user_funds:
    #     price = agent.get_fund_info(symbol)
    #     prices.append(price)

    raise NotImplementedError

    return prices

def test(user_funds):
    """ test method for console """
    prices = download_fund_prices(user_funds)
    for price in prices:
        print(price.identifier, price.date, price.value, price.name)

###########################################################
if __name__ == "__main__":
    #funds = ["8123", "8146", "8148", "8147"]
    funds = ["VANGUARD.BOND", "VANGUARD.HINT", "VANGUARD.HY", "VANGUARD.PROP"]
    test(funds)
