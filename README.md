# gnucash-portfolio

A collection of tools for managing an investment portfolio in GnuCash

User-oriented documentation is at http://portfolio.alensiljak.tk

The purpose of the project is to provide tools that help in managing an investment portfolio in a GnuCash book.
The code is (mostly) written in Python.

## Development

My development environment in on Windows and consists of the following:

- Visual Studio Code with
  - Python extension
  - ctags
- Python 3.6
- node + npm

All the libraries are listed in `requirements.txt` for Python and `package.json` for node.

## Running

### Preparation

- Config: In order to run the scripts, copy `settings.json.template` into `settings.json` and customize the settings by editing the file.
- Register the library with ```pip install -e <path to>/gnucash-portfolio``` as it is called from the reports.

### Execution

All the functionality will be provided as a web application (see below). There are parts of code that are not yet exposed through the web interface, though.

# Web Application

This project contains the web application implemented in Flask. It is intended to be used as the full GUI for accepting user input (parameters) and displaying the output.

The app is located in the /app directory.

It is intended to run on a desktop workstation, with direct access to the GnuCash book file, stored as an SQLite database.

## Benefits

Considering several factors below, it might be preferrable to use an independent application to work with Portfolio then to provide the UI functionality through GnuCash reports using gnucash_utilities project. This approach would utilize the gnucash book/database directly.

- Ease of development  
Developing reports on piecash stack seems fairly straightforward and much simpler than Scheme, GnuCash reporting engine. The control of the output is also easier by directly editing HTML templates and CSS styles.

- Performance  
Comparing the output through GnuCash reports on Windows to the output produced using the Python stack (flask + jinja HTML output + piecash), the advantage is significantly on the side of the Python components.

## Compiling

All the commands for setting up the web app are run from the /app directory.
To get the required development and runtime dependencies, run

`npm install`
`pip install -r requirements.txt`

in the app directory.
Besides this, piecash, and gnucash_portfolio packages must be installed.

### CSS

SCSS is compiled using node-sass:

`npm run css`

### JS

JavaScript is bundled through Flask Assets. It collects the vendor code from installed development node modules. Make sure all the npm dependencies are installed in order for this to work.
The bundle will be built automatically during the app runtime. No additional actions required by the user.

## Running the web app

There are two ways to run the web app:

1. Run `app.py` directly
2. Run "run.py run"

The second script was created so that the app could be debugged with Python extension for Visual Studio Code.

# Reports

An approach using gnucash_utilities project is found in the /reports directory.

The basic idea here is to have GnuCash open a custom report, which runs a Python script, which generates an HTML output.
Gnucash_utilities project provides utilities that generate the Scheme links in the user profile directory. You need to create the Python scripts, which return the HTML output generated with Jinja templates (or any other).

This approach has been abandoned due to the performance benefit of using the web app directly for all data input and output.
