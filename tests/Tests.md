Just a few notes about running tests:

```
pytest -s test_book.py::TestBook_access_book::test_commodity_quantity
```

-s = do not capture output. Useful for printing from the tests.

Specify file::class::method to execute a specific test.
