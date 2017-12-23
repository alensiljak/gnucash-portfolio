:: Lint the whole App
@echo off

pylint ..\app\ --output-format=colorized

pylint ..\gnucash_portfolio\ --output-format=colorized

pause