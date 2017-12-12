"""
This is the entry point to the application
"""
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from gnucash_portfolio import get_vanguard_au_prices
from gnucash_portfolio.lib import portfoliovalue as pvalue, database
# Controllers/blueprints
from controllers import vanguard, income, assetallocation, index

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static')
# Configurations
app.config.from_object('config')
# Register blueprints
app.register_blueprint(index.index_controller)
app.register_blueprint(assetallocation.assetallocation_controller)
app.register_blueprint(vanguard.vanguard_controller)
app.register_blueprint(income.income_controller)

# Bundles
bundles = {
    'home_css': Bundle(
        '../node_modules/@fortawesome/fontawesome/styles.css',
        output='vendor.css'),
}
assets = Environment(app)
assets.register(bundles)


@app.route('/portfoliovalue')
#@templated()
def portfoliovalue():
    """ Portfolio Value report """
    stock_rows = []
    with database.Database().open_book() as book:
        all_stocks = pvalue.get_all_stocks(book)
        #print("found ", len(all_stocks), "records")
        for stock in all_stocks:
            model = pvalue.get_stock_model_from(book, stock)
            stock_rows.append(model)

    # print(stock_rows)
    return render_template('portfolio_value.html', stock_rows=stock_rows)
    # return dict(stock_rows=stock_rows)


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
