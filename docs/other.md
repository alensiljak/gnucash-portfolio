<style>
body {
    background-color: #ccdfcb;
}
</style>

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

## GUI

### Web

- Flask server + jinja2 templates

### Charts

- [pandas](http://pandas.pydata.org/), library for data analysis. Check DataFrame and [exports](http://piecash.readthedocs.io/en/latest/api/piecash.core.book.html#piecash.core.book.Book.splits_df) from piecash.
- [plot.ly](https://plot.ly), plotting service/library with offline Python bindings. For data presentation.
    - [dash](https://plot.ly/products/dash/) framework for analytics.
    - [plotly Python](https://plot.ly/python/)

### Desktop

There are several options for Python GUI.

- [Kivy](https://kivy.org). Multiplatform.
    - [Installation instructions](https://kivy.org/docs/installation/installation-windows.html)
- GTK. GTK, Gio. See [First steps with GSettings](https://blog.gtk.org/2017/05/01/first-steps-with-gsettings/).
    - See [PyGObject](http://pygobject.readthedocs.io/en/latest/getting_started.html)
    - [GAction](https://wiki.gnome.org/HowDoI/GAction)

### Android

In order to use the available functionality, Python scripts can also be run on a mobile device. 
There are several options available (and require further examination). There is a comparison [page](https://wiki.python.org/moin/Android) available at python.org.

- [Kivy](https://kivy.org/docs/guide/android.html)
    - python 4 android [repo]](https://github.com/kivy/python-for-android)
    - p4a [docs](https://python-for-android.readthedocs.io)
- [chaquopy](https://chaquo.com/chaquopy/)
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

The approach using a specialized reporting engine seems to be dying off as HTML is more than capable of providing a decent visual representation of the data.

- [Next Reports](http://www.next-reports.com/products/nextreports-designer.html)
- [Data Vision](http://datavision.sourceforge.net/)
- [Top 7 open source business intelligence and reporting tools](https://opensource.com/business/16/6/top-business-intelligence-reporting-tools)
- [Metabase](https://www.metabase.com/)
- [Dynamic Reports](http://www.dynamicreports.org/)
