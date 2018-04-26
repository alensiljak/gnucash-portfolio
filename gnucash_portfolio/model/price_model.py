"""
Represents a price.
"""
from datetime import datetime
from decimal import Decimal


class PriceModel_Csv:
    """ Price model """
    def __init__(self, symbol=None, currency=None, value: Decimal = None,
                 rate_date: datetime = None):
        if rate_date:
            assert isinstance(rate_date, datetime)
        self.date: datetime = rate_date      # datetime.today().date

        if value:
            assert isinstance(value, Decimal)
        self.value: Decimal = value      # Decimal(0)
        self.symbol: str = symbol        #"AUD" or "AMS:VEUR"
        self.currency: str = currency    #"EUR"

    def parse_euro_date(self, date_string: str):
        """ Parses dd/MM/yyyy dates """
        self.date = datetime.strptime(date_string, "%d/%m/%Y")
        return self.date

    def parse_value(self, value_string: str):
        """
        Parses the amount string.
        """
        self.value = Decimal(value_string)
        return self.value

    def parse(self, csv_row: str):
        """ Parses the .csv row into own values """
        self.date = self.parse_euro_date(csv_row[2])
        self.symbol = csv_row[0]
        self.value = self.parse_value(csv_row[1])
        return self
