# gnucash-portfolio
A collection of tools for managing a portfolio with GnuCash

The purpose of the project is to provide tools that help in managing a portfolio in GnuCash.
The code will mostly be written in Python.

Initially, [MoneyManagerEx for Android](http://android.moneymanagerex.org/) will be used to download the current prices for securities. This provides .csv files with the latest prices. Effectively, this is used instead of Finance::Quote library.

Retrieving currency exchange rates will be part of this suite.

## Running

In order to run the scripts, copy `settings.json.template` into `settings.json` and customize the settings by editing the file.

## To Do

- [] download currency exchange rates
- [] import .csv exchange rates into GnuCash file
- [] import .csv security prices into GnuCash file
- [] display currency pair chart over selected period (report?)
- [] display security price over selected period (report?)
- [] list all dividends for security (?!). This requires some conventions as to where to expect them since there is no direct linking between a commodity and the dividends/interest it earns.
- [] Asset Allocation. This is implemented in MoneyManagerEx for Android and there needs to be a more universal option available. Look into running Python scripts on Android.

## Related Projects

- [gnucash-utilities](https://github.com/sdementen/gnucash-utilities). The underlying utilities.
- [piecash](https://github.com/sdementen/piecash). Access to GnuCash database.
- [Fixerio](http://fixerio.readthedocs.io/en/latest/). Fixer API for currency rates.

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
