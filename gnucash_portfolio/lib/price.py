"""
Represents a price.
"""
import datetime
import dateutil
from decimal import Decimal

class Price:
    """ Price model """
    # Example values
    date = datetime.date.today()
    value = 18.23
    name = "AUD"
    currency = "EUR"

    def parse_euro_date(self, date_string: str):
        """
        Parses dd/MM/yyyy dates.
        """
        #dateutil.parser.parse(date_string,)
        #d = datetime.datetime.strptime( "2012-10-09T19:00:55Z", "%Y-%m-%dT%H:%M:%SZ")
        self.date = datetime.datetime.strptime(date_string, "%d/%m/%Y")
        return self.date

    def parse_value(self, value_string: str):
        """
        Parses the amount string.
        """
        #self.value = float(value_string)
        self.value = Decimal(value_string)
        return self.value
