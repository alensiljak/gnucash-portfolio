"""
The purpose of this module is to test the usage of in-memory, temporary database.
The in-memory database is to be used for fast execution of tests.
"""
from gnucash_portfolio.lib.database import Database
from gnucash_portfolio.bookaggregate import BookAggregate

IN_MEMORY_DB = ":memory:"
IN_MEMORY_DRIVER = "sqlite"

def test_generation():
    """ Test database generation """
    with Database().create_book() as book:
        #assert book.default_currency.mnemonic == "EUR"
        assert book.uri.database == IN_MEMORY_DB
        assert book.uri.drivername == IN_MEMORY_DRIVER

def test_inmemory_db_with_aggregate():
    """ An in-memory database should be also created with the Book Aggregate """
    with BookAggregate() as svc:
        assert svc.book.uri.database == IN_MEMORY_DB
        assert svc.book.uri.drivername == IN_MEMORY_DRIVER
