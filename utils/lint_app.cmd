:: Lint the whole App
@echo off
cls

pylint app --output-format=colorized

pylint gnucash_portfolio --output-format=colorized

::pause