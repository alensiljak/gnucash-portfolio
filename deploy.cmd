:: This script can be used for distribution of Python modules.
:: It automates the compilation of the package and pushes it to the test and prod PyPi servers.
:: Requires twine. 
:: For convenience, also use keyring. Configure credentials for the servers below.
::   `keyring set https://test.pypi.org/legacy/ your-username`
:: [keyring support](https://twine.readthedocs.io/en/latest/#keyring-support).
@echo off

:: Clean-up the destination
del /Q dist\*

:: Create the binary package.
setup.py sdist bdist_wheel

:: Deploy to test server.
echo Deploying to test server =>
twine upload -u cicko --repository-url https://test.pypi.org/legacy/ dist/*

echo About to deploy to Production!
pause

:: Deploy to prod server.
twine upload -u cicko --repository-url https://upload.pypi.org/legacy/ dist/*
