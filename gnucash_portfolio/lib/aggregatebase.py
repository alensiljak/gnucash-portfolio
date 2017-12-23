"""
Base for all aggregates
"""

from abc import ABCMeta
from piecash import Book


class AggregateBase(metaclass=ABCMeta):
    #pass

    def __init__(self, book: Book):
        self.book = book
