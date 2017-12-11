<style>
body {
    background-color: #ccdfcb;
}
</style>

# GnuCash Portfolio

This project adds portfolio management functionality to a GnuCash book saved as an SQLite database.

There is a gratification that comes from the sense of freedom, of having direct access to one's financial data and being able to retrieve any statistic or information one might want, and not depending on others for it.

The project consists of two major area: reports and operations.

Retrieving currency exchange rates is a part of this suite.

## Reports

The initial idea was to provide reports based on the data available in the book.

- portfolio value report
- price charts for currencies and securities
- asset allocation

## Operations

As Python allowed fast development of functions and web interface is so easy and practical, the idea expanded to provide extension of GnuCash functionality through a web app.

Some operations that are targeted:

- import currency exchange rates
- import security prices
- maintain asset allocation

# Goals

## Implemented

- [x] download currency exchange rates
- [x] import exchange rates into GnuCash file
- [x] import .csv security prices into GnuCash file
- [x] securities report
- [x] create a library of callable functions, to be used from the reports.
- [x] list all dividends for security. This requires some conventions as to where to expect them since there is no direct linking between a commodity and the dividends/interest it earns. Search all accounts with the same name in the Income tree.

## To Do

- [ ] Asset Allocation. This is currently implemented in MoneyManagerEx for Android and there should be a version that works with GnuCash book directly. 
- [ ] Charts:
    - [ ] display currency pair chart over selected period (report?)
    - [ ] display security price over selected period (report?)

[Other](other)