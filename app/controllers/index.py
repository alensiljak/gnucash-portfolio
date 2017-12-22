"""
Home controller
"""
from flask import Blueprint, render_template #, request

index_controller = Blueprint('index_controller', __name__)


@index_controller.route('/')
def index():
    """ The default route. Homepage. """
    return render_template('index.html')
