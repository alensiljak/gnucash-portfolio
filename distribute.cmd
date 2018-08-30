:: This script can be used for distribution of Python modules.
:: It automates the compilation of the package and pushes it to the test and prod PyPi servers.
:: Requires twine. 
:: For convenience, also use keyring. Configure credentials for the servers below.
::   `keyring set https://test.pypi.org/legacy/ your-username`
:: [keyring support](https://twine.readthedocs.io/en/latest/#keyring-support).

:: Clean-up the destination
del dist\*
pause

:: Create the binary package.
setup.py sdist bdist_wheel

pause

:: Deploy to test server.
twine upload -u cicko --repository-url https://test.pypi.org/legacy/ dist/*

pause

:: Deploy to prod server.
twine upload -u cicko --repository-url https://upload.pypi.org/legacy/ dist/*
