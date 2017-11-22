"""
Simplest report example.
"""
import sys
from piecash_utilities.report import report, execute_report

@report(
    title="My simplest report",
    name="piecash-simple-report",
    menu_tip="This simple report ever",
    options_default_section="general",
)
def generate_report(
        book_url,
):
    return f"""<html><body>
        Hello world from python !
        <p>
            The current file: {book_url}
        </p>
    </body></html>"""

####################################################################
if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
