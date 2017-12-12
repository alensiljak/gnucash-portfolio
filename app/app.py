"""
This is the entry point to the application
"""
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from gnucash_portfolio import get_vanguard_au_prices

# Controllers/blueprints
from controllers import vanguard, income, assetallocation, index, portfolio, securities

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static')
# Configurations
app.config.from_object('config')
# Register blueprints
app.register_blueprint(index.index_controller)
app.register_blueprint(assetallocation.assetallocation_controller)
app.register_blueprint(vanguard.vanguard_controller)
app.register_blueprint(income.income_controller)
app.register_blueprint(portfolio.portfolio_controller),
app.register_blueprint(securities.stock_controller)

# Bundles
bundles = {
    'vendor_css': Bundle(
        '../node_modules/@fortawesome/fontawesome/styles.css',
        '../node_modules/daterangepicker/daterangepicker.css',
        output='vendor.css'),
    'vendor_js': Bundle(
        '../node_modules/daterangepicker/daterangepicker.js',
        output='vendor.js')
    # 'site_css': Bundle(
    #     'site.scss',
    #     filters='pyscss',
    #     output='site.css')
}
assets = Environment(app)
assets.register(bundles)


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
