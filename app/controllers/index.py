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
