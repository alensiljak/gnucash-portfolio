# Tests

Just a few notes about running tests.

A command like:

```
pytest -s test_book.py::TestBook_access_book::test_commodity_quantity
```

-s = do not capture output. Useful for printing from the tests.

Specify file::class::method to execute a specific test.

## Configuration

Tests are configured in pytest.ini in the root folder.

## Running

With the configuration file, it is enough to run `pytest` anywhere in the project tree. It will read the configuration to find the tests directory and then run all the test files by convention (containing test_* or *_test).

# Packages

pytest package is required for executing unit tests.

# Links

- [Start here](http://pythontesting.net/start-here/)
