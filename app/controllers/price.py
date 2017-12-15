""" Price controller """
from flask import Blueprint, request, render_template

price_controller = Blueprint('price_controller', __name__, url_prefix='/price')

@price_controller.route('/')
def index():
    """ Index page for prices """
    return render_template('incomplete.html')

@price_controller.route('/import')
def import_prices():
    """ Stock price import """
    return render_template('incomplete.html')

@price_controller.route('/importrates')
def import_rates():
    """ Import currency exchange rates """
    # this could be the same, or?
    return render_template('incomplete.html')
