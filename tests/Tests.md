# Tests

Just a few notes about running tests.

A command like:

```
pytest -s test_book.py::TestBook_access_book::test_commodity_quantity
```

-s = do not capture output. Useful for printing from the tests.

Specify file::class::method to execute a specific test.

# Packages

pytest package is required for executing unit tests.

# Links

- [Start here](http://pythontesting.net/start-here/)