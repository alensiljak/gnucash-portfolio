"""
Test security info report
"""
from gnucash_portfolio import BookAggregate
from gnucash_portfolio.reports.security_info import SecurityInfoReport


def test_security_info_report():
    """ debug the report generation """
    book = BookAggregate()
    report = SecurityInfoReport(book)
    # IPE has some capital returns.
    result = report.run("IPE")

    assert result is not None
