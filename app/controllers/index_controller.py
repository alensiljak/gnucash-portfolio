"""
Index/Home controller
"""
#from logging import log, DEBUG, INFO, WARN, ERROR, FATAL
from flask import Blueprint, render_template #, request


index_controller = Blueprint( # pylint: disable=invalid-name
    'index_controller', __name__)

@index_controller.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')

@index_controller.route('/components')
def components():
    return render_template('components.html')
