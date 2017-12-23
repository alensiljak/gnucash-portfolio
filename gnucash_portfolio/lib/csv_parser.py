""" Parse CSV into prices and rates """

from logging import log, DEBUG
from typing import List
import csv
from gnucash_portfolio.model.price_model import PriceModel


def parse_prices_from_file_stream(file_stream) -> List[PriceModel]:
    """
    Reads a file stream (i.e. from web form) containing a csv prices
    into a list of Price models.
    """
    content = file_stream.read().decode("utf-8")
    file_stream.close()

    if not content:
        raise ValueError("The file is empty!")

    result = get_prices_from_csv(content)

    return result


def get_prices_from_csv(content: str) -> List[PriceModel]:
    """ Imports prices from CSV content. See data folder for a sample file/content. """
    lines = content.splitlines()
    prices = []

    reader = csv.reader(lines)
    for row in reader:
        price = PriceModel().parse(row)
        log(DEBUG, "parsed price. date is %s", price.date)
        #price.currency = "EUR"

        prices.append(price)
    return prices
