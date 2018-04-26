:: Lint the whole App
@echo off
cls

pylint gnucash_portfolio --output-format=colorized

::pause