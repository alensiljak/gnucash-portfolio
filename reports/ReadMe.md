# Reports

Here are the reports that can be used through `gnucash-utilities` bridge.
These are to be placed, together with their subfolder, in your <profile dir>\.gnucash folder.
i.e.:

```
C:\Users\me\.gnucash\report_simple\report_simple.py
```
After placing the reports in the correct location, run ```gc_report``` to generate the resulting report (.scm) files for GnuCash.

# gnucash-utilities

The ```gc_report_create <name-of-report>``` script will generate a sample report in .gnucash directory, together with an HTML template.
The jinja template has options for iterating through the lists and calculating values.
