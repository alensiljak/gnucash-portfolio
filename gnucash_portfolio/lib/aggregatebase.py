"""
Base for all aggregates
"""

from abc import ABCMeta
from piecash import Book
#import logging


class AggregateBase(metaclass=ABCMeta):
    """ Base for the aggregates """
    def __init__(self, book: Book):
        self.book = book
        #self._logger = logging.Logger
