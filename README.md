# gnucash-portfolio

A collection of tools for managing an investment portfolio in GnuCash

User-oriented documentation is at http://portfolio.alensiljak.tk

## Introduction

The purpose of the project is to provide tools that help in managing an investment portfolio in a GnuCash book.
The code is written in Python.

## Development Environment

The development environment should include the following:

- Python IDE (vscode or pycharm)
- Python 3.6
- node + npm

All the libraries are listed in `requirements.txt`.

## Set-Up

To install the required development and runtime dependencies, run

```
pip install -r requirements.txt
```

in the root and app directory since requirements.txt is in the project root.

The local/development versions of any library can be registered with

`pip install -e <path>`

i.e.

`pip install -e .`

### Configuration

Go to config directory and copy the config.json.template file into `config.json`. Adjust any values as needed. This file can also be edited by going to the Settings option in the web app (webgui).

## Testing

See `tests` directory and documentation and tests there.
Simply run

`pytest`

to run all tests.

### Lint

pylint can be used to check for errors. You can check the code by doing the following:

- run `utils\lint_app.cmd` from project root directory,
- run lint tasks from vscode,
- run `pylint gnucash_portfolio` to check the library.

Pay attention to the Error and Fatal lines. See utils/lint_app.cmd script for coloring output.

Ref: [PyLint Output](https://docs.pylint.org/en/1.6.0/output.html)

# Reports

An approach using gnucash_utilities project is found in the /reports directory.

The basic idea here is to have GnuCash open a custom report, which runs a Python script, which generates an HTML output.
Gnucash_utilities project provides utilities that generate the Scheme links in the user profile directory. You need to create the Python scripts, which return the HTML output generated with Jinja templates (or any other).

This approach has been abandoned due to the performance benefit of using the web app directly for all data input and output.

# Distribution

## Test Site

```console
python setup.py sdist upload -r test
```

## Production Site

```console
python setup.py sdist upload -r pypi
```