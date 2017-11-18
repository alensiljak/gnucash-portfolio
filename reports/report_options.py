"""
Example on how to pass options to the report.
http://gnucash-utilities.readthedocs.io/en/stable/doc/doc.html
"""
import sys
from piecash_utilities.report import report, RangeOption, DateOption, StringOption, execute_report


@report(
    title="My simplest report with parameters",
    name="piecash-simple-report-parameters",
    menu_tip="A simple report with parameters",
    options_default_section="general",
)
def generate_report(
        book_url,
        a_number: RangeOption(
            section="main",
            sort_tag="a",
            documentation_string="This is a number",
            default_value=3),
        a_str: StringOption(
            section="main",
            sort_tag="c",
            documentation_string="This is a string",
            default_value="with a default value"),
        a_date: DateOption(
            section="main",
            sort_tag="d",
            documentation_string="This is a date",
            default_value="(lambda () (cons 'absolute (cons (current-time) 0)))"),
        another_number: RangeOption(
            section="main",
            sort_tag="b",
            documentation_string="This is a number",
            default_value=3)
):
    return f"""<html>
    <body>
        Hello world from python !<br>
        Using book: {book_url} <br/>
        Parameters received:<br>
        <ul>
        <li>a_number = {a_number}</li>
        <li>a_str = {a_str}</li>
        <li>a_date = {a_date}</li>
        <li>another_number = {another_number}</li>
        </ul>
    </body>
    </html>"""


if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
