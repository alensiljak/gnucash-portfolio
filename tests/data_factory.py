#!/usr/bin/python3
""" Generation of test data for in-memory database """

from piecash import Commodity

def create_currency(symbol: str):
    """ Creates a currency """
    cur = Commodity("CURRENCY", symbol, fullname="Australian Dollar")
    return cur
