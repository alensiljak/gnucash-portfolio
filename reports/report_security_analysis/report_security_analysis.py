#!/usr/bin/env python
"""
Security Analysis
Displays the quantity of the selected commodity and the average price paid.
"""
import sys
import os
import piecash
from piecash_utilities.report import report, execute_report

####################################################################
@report(
    title="Security Analysis",
    name="security-analysis-report",
    menu_tip="Security details",
    options_default_section="general",
)
def generate_report(book_url):
    """
    Generates an HTML report content.
    """
    #with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        #print(book.default_currency)

    # Load HTML template file.
    template = load_html_template()
    return template.format(**locals())

    # return f"""<html><body>
    #     <h1>Security Analysis</h1>
    #     Hello world from python !
    #     <p>
    #         The current file: {book_url}
    #     </p>
    # </body></html>"""

def load_html_template():
    """
    Loads the template from a file. This makes it easier to edit the template in an editor.
    """
    script_path = os.path.dirname(os.path.realpath(__file__))
    #print(script_path)

    template_file_name = "template.html"
    #file_path = os.path.relpath()
    #file_path = os.path.abspath()
    file_path = os.path.join(script_path, template_file_name)
    #print(file_path)

    with open(file_path, 'r') as template_file:
        return template_file.read()


####################################################################
if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
