""" Parse CSV into prices and rates """

from typing import List
import csv
from pricedb import PriceModel


class CsvPriceParser:
    """ Parses .csv into list of prices """

    def __init__(self, currency: str):
        self.currency = currency

    def parse_prices_from_file_stream(self, file_stream) -> List[PriceModel]:
        """
        Reads a file stream (i.e. from web form) containing a csv prices
        into a list of Price models.
        """
        content = file_stream.read().decode("utf-8")
        file_stream.close()

        if not content:
            raise ValueError("The file is empty!")

        result = self.get_prices_from_csv(content)

        return result

    def get_prices_from_csv(self, content: str) -> List[PriceModel]:
        """ Imports prices from CSV content. See data folder for a sample file/content. """
        lines = content.splitlines()
        prices = []

        reader = csv.reader(lines)
        for row in reader:
            price = PriceModel().parse(row)
            price.currency = self.currency

            prices.append(price)
        return prices
