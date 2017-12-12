"""
Account operations
- search
- editing of metadata (?)
- list of transactions / register -> see transaction controller
"""
from flask import Blueprint, request, render_template

account_controller = Blueprint('account_controller', __name__, url_prefix='/account')

@account_controller.route('/')
def index():
    return render_template('incomplete.html')

@account_controller.route('/search')
def search():
    return render_template('incomplete.html')
