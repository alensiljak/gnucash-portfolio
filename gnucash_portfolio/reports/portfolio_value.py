""" Portfolio Value report """

from pydatum import Datum
from gnucash_portfolio import BookAggregate
from gnucash_portfolio.lib import portfoliovalue, datetimeutils
from gnucash_portfolio.reports.portfolio_models import PortfolioValueInputModel, PortfolioValueViewModel
from gnucash_portfolio.model.stock_model import StockViewModel


def run(input_model: PortfolioValueInputModel):
    """ Fetch the report data """
    model = __get_model_for_portfolio_value(input_model)
    return model


def __get_model_for_portfolio_value(input_model: PortfolioValueInputModel) -> PortfolioValueViewModel:
    """ loads the data for portfolio value """
    result = PortfolioValueViewModel()
    result.filter = input_model

    ref_datum = Datum()
    ref_datum.from_datetime(input_model.as_of_date)
    ref_date = ref_datum.end_of_day()

    result.stock_rows = []
    with BookAggregate() as svc:
        book = svc.book
        stocks_svc = svc.securities

        if input_model.stock:
            symbols = input_model.stock.split(",")
            stocks = stocks_svc.get_stocks(symbols)
        else:
            # stocks = portfoliovalue.get_all_stocks(book)
            stocks = stocks_svc.get_all()

        for stock in stocks:
            row: StockViewModel = portfoliovalue.get_stock_model_from(
                book, stock, as_of_date=ref_date)
            if row:
                result.stock_rows.append(row)

    return result

if __name__ == "__main__":
    run(input_model=None)
