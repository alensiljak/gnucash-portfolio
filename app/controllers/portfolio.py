"""
Portfolio
- cash account balances per currency
- portfolio value report
"""
from datetime import date, datetime, timedelta
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import portfoliovalue, database
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securityaggregate import SecurityAggregate, SecuritiesAggregate

portfolio_controller = Blueprint('portfolio_controller', __name__, 
                                 url_prefix='/portfolio')


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
    input_model = __parse_input_model(request)

    model = __get_model_for_portfolio_value(input_model)
    return render_template('portfolio.value.html', model=model)


class PortfolioValueInputModel:
    """ Input model for portfolio value filter parameters """
    def __init__(self):
        today = datetime.today()
        self.as_of_date: datetime = datetime(today.year, today.month, today.day)
        self.stock = ""

class PortfolioValueViewModel:
    """ View Model for portfolio value report """
    def __init__(self):
        self.filter = None
        self.stock_rows = []


def __get_model_for_portfolio_value(input_model: PortfolioValueInputModel):
    """ loads the data for portfolio value """
    result = PortfolioValueViewModel()
    result.filter = input_model

    result.stock_rows = []
    with BookAggregate() as svc:
        book = svc.book
        if input_model.stock:
            symbols = input_model.stock.split(",")
            stocks_svc = SecuritiesAggregate(book)
            stocks = stocks_svc.get_stocks(symbols)
        else:
            stocks = portfoliovalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in stocks:
            row = portfoliovalue.get_stock_model_from(
                book, stock, as_of_date=input_model.as_of_date)
            result.stock_rows.append(row)

    return result

def __parse_input_model(request) -> PortfolioValueInputModel:
    """ Parses the search parameters from the request """
    result = PortfolioValueInputModel()

    date_input_str = request.form.get("filter.as_of_date")
    date_input = datetime.strptime(date_input_str, "%Y-%m-%d")
    result.as_of_date = datetime(date_input.year, date_input.month, date_input.day, 23, 59, 59)

    result.stock = request.form.get("filter.stock")

    return result
