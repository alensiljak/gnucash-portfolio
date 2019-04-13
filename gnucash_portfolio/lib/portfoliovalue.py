"""
Provides functions for Portfolio Value report
"""
from datetime import date
from piecash import Book, Commodity
from pricedb import PriceModel

from gnucash_portfolio.actions import symbol_dividends
from gnucash_portfolio.pricesaggregate import PricesAggregate
from gnucash_portfolio.securitiesaggregate import SecurityAggregate
from gnucash_portfolio.model.stock_model import StockViewModel


def get_stock_model_from(book: Book, commodity: Commodity, as_of_date: date) -> StockViewModel:
    """ Parses stock/commodity and returns the model for display """
    from decimal import Decimal
    from pydatum import Datum

    svc = SecurityAggregate(book, commodity)
    model = StockViewModel()

    model.exchange = commodity.namespace
    model.symbol = commodity.mnemonic

    model.shares_num = svc.get_num_shares_on(as_of_date)
    # Ignore 0-balance
    if model.shares_num == 0:
        return None

    model.avg_price = svc.get_avg_price()

    # Last price
    price_svc = PricesAggregate(book)
    # last_price: Price = price_svc.get_price_as_of(commodity, as_of_date)
    last_price: PriceModel = price_svc.get_latest_price(commodity)
    if last_price is not None:
        model.price = last_price.value
    else:
        model.price = Decimal(0)

    # currency
    if model.price:
        model.currency = last_price.currency

    # Cost
    model.cost = model.shares_num * model.avg_price

    # Balance (current value)
    if model.shares_num > 0 and model.price:
        model.balance = model.shares_num * model.price
    else:
        model.balance = Decimal(0)

    # Gain/Loss
    model.gain_loss = model.balance - model.cost

    # Gain/loss percentage
    gain_loss_perc = 0
    if model.cost:
        gain_loss_perc = abs(model.gain_loss) * 100 / model.cost
        if model.gain_loss < 0:
            gain_loss_perc *= -1
    model.gain_loss_perc = gain_loss_perc

    # Income
    income = symbol_dividends.get_dividend_sum_for_symbol(book, model.symbol)
    model.income = float(income)

    #income_12m = symbol_dividends.
    start = Datum()
    start.subtract_months(12)
    end = Datum()
    model.income_last_12m = svc.get_income_in_period(start, end)
    if model.balance > 0 and model.income_last_12m > 0:
        model.income_last_12m_perc = model.income_last_12m * 100 / model.balance
    else:
        model.income_last_12m_perc = Decimal(0)

    return model
