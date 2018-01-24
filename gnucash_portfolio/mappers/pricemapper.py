""" Mapper for the Price entity """

from piecash import Price
from gnucash_portfolio.model.price_model import PriceModel

class PriceMapper:
    """ Map the Price entity to allow modifying the values without the engine trying
    to persist them to the database """

    def map_price(self, price: Price) -> PriceModel:
        """ Map to price model """
        pass
