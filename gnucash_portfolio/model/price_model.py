"""
Represents a price.
"""
from datetime import datetime
from decimal import Decimal


class PriceModel:
    """ Price model """
    def __init__(self):
        self.date: datetime = None  # datetime.today()
        self.value: Decimal = None  # Decimal(0)
        self.name: str = None       #"AUD"
        self.currency: str = None   #"EUR"


    def parse_euro_date(self, date_string: str):
        """
        Parses dd/MM/yyyy dates.
        """
        #dateutil.parser.parse(date_string,)
        #d = datetime.datetime.strptime( "2012-10-09T19:00:55Z", "%Y-%m-%dT%H:%M:%SZ")
        self.date = datetime.strptime(date_string, "%d/%m/%Y")
        return self.date


    def parse_value(self, value_string: str):
        """
        Parses the amount string.
        """
        #self.value = float(value_string)
        self.value = Decimal(value_string)
        return self.value

    def parse(self, csv_row: str):
        """ Parses the .csv row into own values """
        self.date = self.parse_euro_date(csv_row[2])
        self.name = csv_row[0]
        self.value = self.parse_value(csv_row[1])
        return self
