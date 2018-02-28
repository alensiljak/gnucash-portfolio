"""
Base for all aggregates
"""

from abc import ABCMeta
from piecash import Book


class AggregateBase(metaclass=ABCMeta):
    """ Base for the aggregates """
    def __init__(self, book: Book):
        self.book = book
