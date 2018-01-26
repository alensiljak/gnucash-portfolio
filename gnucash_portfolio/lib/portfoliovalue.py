"""
Provides functions for Portfolio Value report
"""
#from logging import log, DEBUG
from datetime import date
from typing import List
from piecash import Book, Commodity, Price
from gnucash_portfolio.actions import symbol_dividends
from gnucash_portfolio.pricesaggregate import PricesAggregate
from gnucash_portfolio.securities import SecurityAggregate
from gnucash_portfolio.model.stock_model import StockViewModel


def get_stock_model_from(book: Book, commodity: Commodity, as_of_date: date):
    """ Parses stock/commodity and returns the model for display """

    model = StockViewModel()

    model.exchange = commodity.namespace
    model.symbol = commodity.mnemonic

    svc = SecurityAggregate(book, commodity)

    model.shares_num = svc.get_num_shares_on(as_of_date)
    # Ignore 0-balance
    if model.shares_num == 0:
        return None

    model.avg_price = svc.get_avg_price()

    # Last price
    price_svc = PricesAggregate(book)
    last_price: Price = price_svc.get_price_as_of(commodity, as_of_date)
    if last_price is not None:
        model.price = last_price.value
    #print("last price", last_price.value, last_price.currency.mnemonic)

    # currency
    if model.price:
        model.currency = last_price.currency.mnemonic

    # Cost
    model.cost = model.shares_num * model.avg_price

    # Balance
    if model.shares_num and model.price:
        model.balance = model.shares_num * model.price

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

    return model
