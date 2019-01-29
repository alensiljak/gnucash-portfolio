#!/usr/bin/python3
""" Generation of test data for in-memory database """

from piecash import Commodity, ScheduledTransaction

def create_currency(symbol: str):
    """ Creates a currency """
    cur = Commodity("CURRENCY", symbol, fullname="Australian Dollar")
    return cur

def create_scheduled_tx():
    tx = ScheduledTransaction()
    return tx