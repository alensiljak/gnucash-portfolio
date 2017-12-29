""" This is the entry point to the application """
#import os
from logging.config import dictConfig
from flask import Blueprint, Flask #, send_from_directory
from flask_assets import Bundle, Environment

# Controllers/blueprints
from app.controllers import (
    account_controller, currency_controller, vanguard, distributions_controller,
    assetallocation_controller, index, portfolio_controller, price_controller,
    securities_controller, settings_controller, scheduled_controller, transaction_controller)


# Configure logging before the application is initialized.
# http://flask.pocoo.org/docs/dev/logging/
dictConfig({
    'version': 1,
    'root': {
        # Log all levels to the console.
        'level': 'NOTSET'
    }
})

# pylint: disable=invalid-name

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static') # pylint: disable=invalid-name

# Configurations
app.config.from_object('config')
# Register blueprints
app.register_blueprint(index.index_controller)
app.register_blueprint(account_controller.account_controller)
app.register_blueprint(assetallocation_controller.assetallocation_controller)
app.register_blueprint(currency_controller.currency_controller)
app.register_blueprint(distributions_controller.distribution_controller)
app.register_blueprint(portfolio_controller.portfolio_controller)
app.register_blueprint(price_controller.price_controller)
app.register_blueprint(scheduled_controller.scheduled_controller)
app.register_blueprint(settings_controller.settings_controller)
app.register_blueprint(securities_controller.stock_controller)
app.register_blueprint(transaction_controller.transaction_controller)
app.register_blueprint(vanguard.vanguard_controller)

# Static routes.
scripts_route = Blueprint('scripts', __name__, static_url_path='/scripts',
                          static_folder='scripts')
app.register_blueprint(scripts_route)
fa_route = Blueprint('fa', __name__, static_url_path='/fonts',
                     static_folder='node_modules/font-awesome/fonts')
app.register_blueprint(fa_route)
#images_route = Blueprint('img', __name__, static_url_path='/img', static_folder='img')
# app.register_blueprint(images_route)

# Bundles
bundles = {
    'vendor_css': Bundle(
        #'../node_modules/@fortawesome/fontawesome/styles.css',
        #'../node_modules/@fortawesome/fontawesome-free-solid',
        '../node_modules/font-awesome/css/font-awesome.min.css',
        '../node_modules/daterangepicker/daterangepicker.css',
        '../node_modules/datatables.net-bs4/css/dataTables.bootstrap4.css',
        '../node_modules/select2/dist/css/select2.min.css',
        '../node_modules/chosen-js/chosen.min.css',
        output='vendor.css'),
    'vendor_js': Bundle(
        '../node_modules/popper.js/dist/umd/popper.min.js',
        '../node_modules/jquery/dist/jquery.min.js',
        '../node_modules/moment/min/moment.min.js',
        '../node_modules/daterangepicker/daterangepicker.js',
        '../node_modules/bootstrap/dist/js/bootstrap.min.js',
        '../node_modules/datatables.net/js/jquery.dataTables.js',
        '../node_modules/datatables.net-bs4/js/dataTables.bootstrap4.js',
        '../node_modules/select2/dist/js/select2.min.js',
        '../node_modules/chosen-js/chosen.jquery.min.js',
        '../node_modules/devbridge-autocomplete/dist/jquery.autocomplete.min.js',
        #'../node_modules/react/umd/react.production.min.js',
        '../node_modules/react/umd/react.development.js',
        #'../node_modules/react-dom/umd/react-dom.production.min.js',
        '../node_modules/react-dom/umd/react-dom.development.js',
        '../node_modules/babel-standalone/babel.min.js',
        output='vendor.js'),
    # 'site_css': Bundle(
    #     'site.scss',
    #     filters='pyscss',
    #     output='site.css')
    'site_js': Bundle(
        '../scripts/basic.js',
        output='site.js'
    )
}
assets = Environment(app)
assets.register(bundles)

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(
#         os.path.join(app.root_path, 'static'), 'briefcase.png',
#         mimetype='image/png')

##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    app.run()
