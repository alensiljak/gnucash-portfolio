"""
Portfolio
- cash account balances per currency
- portfolio value report
"""
from datetime import date, datetime, timedelta
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import portfoliovalue, database
from gnucash_portfolio.bookaggregate import BookAggregate

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
    as_of = request.args.get("as_of_date")
    print(as_of)
    input_model = __parse_input_model(request)

    model = __get_model_for_portfolio_value(input_model)
    return render_template('portfolio.value.html', model=model)

class PortfolioValueInputModel:
    """ Input model for portfolio value filter parameters """
    def __init__(self):
        today = datetime.today()
        self.as_of_date: datetime = datetime(today.year, today.month, today.day)

class PortfolioValueViewModel:
    """ View Model for portfolio value report """
    def __init__(self):
        self.search = None
        self.stock_rows = []

def __get_model_for_portfolio_value(input_model: PortfolioValueInputModel):
    """ loads the data for portfolio value """
    result = PortfolioValueViewModel()
    result.search = input_model

    result.stock_rows = []
    with BookAggregate() as svc:
        book = svc.book
        all_stocks = portfoliovalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in all_stocks:
            row = portfoliovalue.get_stock_model_from(
                book, stock, as_of_date=input_model.as_of_date)
            result.stock_rows.append(row)

    return result

def __parse_input_model(request) -> PortfolioValueInputModel:
    """ Parses the search parameters from the request """
    result = PortfolioValueInputModel()

    date_input = request.form.get("as_of_date")
    result.as_of_date = datetime.strptime(date_input, "%Y-%m-%d")

    return result
