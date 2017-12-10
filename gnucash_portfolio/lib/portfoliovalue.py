"""
Provides functions for Portfolio Value report
"""
from sqlalchemy import desc
from piecash import Book, Commodity, Price
import gnucash_portfolio
from gnucash_portfolio import symbol_dividends

def get_stock_model_from(book: Book, commodity: Commodity):
    """ Parses stock/commodity and returns the model for display """
    model = {}

    #security = book.get(Commodity, mnemonic=symbol)
    model["exchange"] = commodity.namespace
    
    symbol = commodity.mnemonic
    model["symbol"] = symbol

    shares_no = gnucash_portfolio.get_number_of_shares(commodity)
    model["shares_no"] = float(shares_no)
    #shares_no_disp = "{:,.2f}".format(shares_no)

    avg_price = gnucash_portfolio.get_avg_price(commodity)
    model["avg_price"] = float(avg_price)
    #avg_price_disp = "{:,.4f}".format(avg_price)

    # Last price
    last_price: Price = commodity.prices.order_by(desc(Price.date)).first()
    price = None
    if last_price is not None:
        price = last_price.value
        model["price"] = float(price)
    #print("last price", last_price.value, last_price.currency.mnemonic)

    # currency
    if price:
        model["currency"] = last_price.currency.mnemonic

    # Cost
    cost = shares_no * avg_price
    model["cost"] = float(cost)

    # Balance
    balance = 0
    if shares_no and price:
        balance = shares_no * price
    model["balance"] = float(balance)

    # Gain/Loss
    gain_loss = balance - cost
    model["gain_loss"] = float(gain_loss)

    # Gain/loss percentage
    gain_loss_perc = 0
    if cost:
        gain_loss_perc = abs(gain_loss) * 100 / cost
        if gain_loss < 0:
            gain_loss_perc *= -1
    model["gain_loss_perc"] = float(gain_loss_perc)

    # Income
    income = symbol_dividends.get_dividend_sum_for_symbol(book, symbol)
    model["income"] = float(income)

    return model

def get_all_stocks(book: Book):
    """ Load all stocks """
    all_stocks = book.session.query(Commodity).filter(Commodity.namespace != "CURRENCY",
                                                    Commodity.mnemonic != "template").order_by(Commodity.mnemonic).all()
    return all_stocks
    