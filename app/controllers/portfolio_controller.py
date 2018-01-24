"""
Portfolio
- cash account balances per currency
- portfolio value report
"""
from datetime import datetime #, timedelta
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import portfoliovalue, datetimeutils
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securitiesaggregate import SecuritiesAggregate
from app.models.portfolio_models import PortfolioValueInputModel, PortfolioValueViewModel

portfolio_controller = Blueprint( # pylint: disable=invalid-name
    'portfolio_controller', __name__, url_prefix='/portfolio')

@portfolio_controller.route('/value', methods=['GET'])
def portfolio_value():
    """ Portfolio Value report """
    # default filter parameters
    search = PortfolioValueInputModel()

    model = __get_model_for_portfolio_value(search)

    return render_template('portfolio.value.html', model=model)

@portfolio_controller.route('/value', methods=['POST'])
def portfolio_value_post():
    """ Accepts the filter parameters and displays the portfolio value report """
    input_model = __parse_input_model()

    model = __get_model_for_portfolio_value(input_model)
    return render_template('portfolio.value.html', model=model)

######################
# Private

def __get_model_for_portfolio_value(input_model: PortfolioValueInputModel):
    """ loads the data for portfolio value """
    result = PortfolioValueViewModel()
    result.filter = input_model

    ref_date = datetimeutils.end_of_day(input_model.as_of_date)

    result.stock_rows = []
    with BookAggregate() as svc:
        book = svc.book
        stocks_svc = SecuritiesAggregate(book)

        if input_model.stock:
            symbols = input_model.stock.split(",")
            stocks = stocks_svc.get_stocks(symbols)
        else:
            # stocks = portfoliovalue.get_all_stocks(book)
            stocks = stocks_svc.get_all()

        for stock in stocks:
            row = portfoliovalue.get_stock_model_from(
                book, stock, as_of_date=ref_date)
            if row:
                result.stock_rows.append(row)

    return result

def __parse_input_model() -> PortfolioValueInputModel:
    """ Parses the search parameters from the request """
    result = PortfolioValueInputModel()

    date_input_str = request.form.get("filter.as_of_date")
    date_input = datetime.strptime(date_input_str, "%Y-%m-%d")
    result.as_of_date = datetime(date_input.year, date_input.month, date_input.day, 23, 59, 59)

    result.stock = request.form.get("security")

    return result
