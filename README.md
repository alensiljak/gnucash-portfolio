# gnucash-portfolio
A collection of tools for managing an investment portfolio in GnuCash

User-oriented documentation is at http://portfolio.alensiljak.tk

The purpose of the project is to provide tools that help in managing an investment portfolio in a GnuCash book.
The code is (mostly) written in Python.

## Running

### Preparation

- Config: In order to run the scripts, copy `settings.json.template` into `settings.json` and customize the settings by editing the file.
- Register the library with 
```
pip install -e <path to>/gnucash-portfolio
```
as it is called from the reports.

### Execution

All the functionality will be provided as a web application. There are parts of code that are not yet exposed through the web interface, though.
Simply run `run.bat` in the app directory.

### Web Application

To prepare the web application, install npm dependencies listed in package.json.
Install Python dependencies in requirements.txt.