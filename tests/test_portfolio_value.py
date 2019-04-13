'''
Test portfolio value report
'''

def test_zero_income():
    ''' debugging test for a symbol that has no income in the last 12mo '''
    from decimal import Decimal
    from gnucash_portfolio.reports.portfolio_value import (run, PortfolioValueInputModel,
                                                           PortfolioValueViewModel)
    from gnucash_portfolio.model.stock_model import StockViewModel

    input_model = PortfolioValueInputModel()
    input_model.stock = 'EMHY'

    result: PortfolioValueViewModel = run(input_model)

    assert result is not None
    row: StockViewModel = result.stock_rows[0]
    perc_12m = row.income_last_12m_perc
    assert perc_12m == Decimal(0)
