# gnucash-portfolio
A collection of tools for managing a portfolio with GnuCash

The purpose of the project is to provide tools that help in managing a portfolio in GnuCash.
The code will mostly be written in Python.

The gratification is the sense of freedom by having direct access to your financial data and being able to retrieve any statistic or information you want, and not depending on others to do it for you.

Retrieving currency exchange rates is a part of this suite.

## Running

- Config: In order to run the scripts, copy `settings.json.template` into `settings.json` and customize the settings by editing the file.
- Register the library with 
```
pip install -e <path to>/gnucash-portfolio
```
as it is called from the reports.

# Goals

## Done

- [x] download currency exchange rates
- [x] import exchange rates into GnuCash file
- [x] import .csv security prices into GnuCash file
- [x] securities report
- [x] create a library of callable functions, to be used from the reports.

## To Do

- [ ] Asset Allocation. This is currently implemented in MoneyManagerEx for Android and there should be a version that works with GnuCash book directly. 
- [ ] Charts:
    - [ ] display currency pair chart over selected period (report?)
    - [ ] display security price over selected period (report?)
- [ ] list all dividends for security (?!). This requires some conventions as to where to expect them since there is no direct linking between a commodity and the dividends/interest it earns. Search all accounts with the same name in the Income tree?
- [ ] Enhance average price calculation. Take into account lots and sold securities. See how selling shares affects the average price.

# Other

## Related Projects

- [MoneyManagerEx for Android](http://android.moneymanagerex.org/) can be used to download the current prices for securities. This provides .csv files with the latest prices. 
- Finance::Quote - The default GnuCash method for fetching commodity prices.
- [gnucash-utilities](https://github.com/sdementen/gnucash-utilities). The suite of tools that provide Python reports for GnuCash data.
- [piecash](https://github.com/sdementen/piecash). Provides access to GnuCash database and schema.
- [Fixerio](http://fixerio.readthedocs.io/en/latest/). Fixer API for online currency rates.

## References

- [GnuCash Wiki](https://wiki.gnucash.org/wiki/GnuCash)
    - [Custom Reports](https://wiki.gnucash.org/wiki/Custom_Reports)

## UI

- [pandas](http://pandas.pydata.org/), library for data analysis. Check DataFrame and [exports](http://piecash.readthedocs.io/en/latest/api/piecash.core.book.html#piecash.core.book.Book.splits_df) from piecash.
- [plot.ly](https://plot.ly), plotting service/library with offline Python bindings. For data presentation.

## GUI

There are several options for Python GUI.

- [Kivy](https://kivy.org). Multiplatform.
    - [Installation instructions](https://kivy.org/docs/installation/installation-windows.html)
- GTK. GTK, Gio. See [First steps with GSettings](https://blog.gtk.org/2017/05/01/first-steps-with-gsettings/).
    - See [PyGObject](http://pygobject.readthedocs.io/en/latest/getting_started.html)
    - [GAction](https://wiki.gnome.org/HowDoI/GAction)


## Python on Android

In order to use the available functionality, Python scripts can also be run on a mobile device. 
There are several options available (and require further examination). There is a comparison [page](https://wiki.python.org/moin/Android) available at python.org.

- [chaquopy](https://chaquo.com/chaquopy/)
- [Kivy](https://kivy.org/docs/guide/android.html)
- [PySide](http://wiki.qt.io/PySide_for_Android_guide) for Android. 
- [QPython](http://www.qpython.com/)
    - [Python 2](https://play.google.com/store/apps/details?id=org.qpython.qpy)
    - [Python 3](https://play.google.com/store/apps/details?id=org.qpython.qpy3)
    - [Community](http://qpython.org/)
    - [repo](https://github.com/qpython-android/qpython)

There are two technologies providing underlying access to Android functions:

- [PyJNIus](http://pyjnius.readthedocs.io/en/latest/)
- [Python for Android: The Scripting Layer (SL4A)](http://pythoncentral.io/python-for-android-the-scripting-layer-sl4a/)

## To Explore

Some related technologies. [Reference](https://groups.google.com/forum/#!topic/piecash/YgrkL1MVL18)

### jinja2

Using piecash+jinja2 could ease the generation of :
- invoices (via latex or other type setting),
- reports (see http://pbpython.com/pdf-reports.html) 
- charts (with https://github.com/ellisonbg/altair or https://plot.ly/)
- export to other formats (xml, ledger http://www.ledger-cli.org/, QIF, ...)

With pandas, you get easy:
- time series analysis (prices, account balances, ...) 
- export of time series to json, csv, xlsx, ...
- plotting

### Pandas DataFrame

You can see an example of a usage of these dataframes to do basic reporting here :
https://nbviewer.jupyter.org/github/sdementen/piecash/blob/master/examples/ipython/piecash_dataframes.ipynb

### Reporting Engines

- [Next Reports](http://www.next-reports.com/products/nextreports-designer.html)
- [Data Vision](http://datavision.sourceforge.net/)
- [Top 7 open source business intelligence and reporting tools](https://opensource.com/business/16/6/top-business-intelligence-reporting-tools)
- [Metabase](https://www.metabase.com/)
- [Dynamic Reports](http://www.dynamicreports.org/)
