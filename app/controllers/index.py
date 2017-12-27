"""
Home controller
"""
#from logging import log, info, debug, DEBUG, INFO, WARN, ERROR, FATAL
from flask import Blueprint, render_template #, request


index_controller = Blueprint( # pylint: disable=invalid-name
    'index_controller', __name__)


@index_controller.route('/')
def index():
    """ The default route. Homepage. """
    #log(DEBUG, "yo!")
    #debug("index page")
    return render_template('index.html')

@index_controller.route('/partial/scheduled')
def scheduled_partial():
    """ Partial for scheduled transactions. Displays ten upcoming transactions
    for the dashboard. """
    return render_template('incomplete.html')
