<style>
body {
    background-color: #ccdfcb;
}
</style>

# GnuCash Portfolio

This project adds portfolio management functionality to a GnuCash book saved as an SQLite database.

There is a gratification that comes from the sense of freedom, of having direct access to one's financial data and being able to retrieve any statistic or information one might want, and not depending on anyone else for it.

The project consists of two major area: reports and operations.

Retrieving currency exchange rates is also part of this suite.

Several sub-projects emerged during development of the suite:

- price database, for storage of security prices
- price-quote, for online retrieval of current security prices
- asset-allocation, for calculation and maintenance of asset allocation

---

[Other](other) * [Links](links) * [User Manual](user_manual) * [ASP.Net MVC](aspnetmvc)

---

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

# Targets

See the [issues list](https://github.com/MisterY/gnucash-portfolio/issues) on GitHub for up-to-date list of implemented and open issues and features.
