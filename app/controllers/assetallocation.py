"""
Asset Allocation controller
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import settings, assetallocation as aalloc

assetallocation_controller = Blueprint('assetallocation_controller', __name__, url_prefix='/assetallocation')

@assetallocation_controller.route('/full')
def assetallocation():
    """ Asset Allocation with stocks """
    book_url = settings.Settings().database_uri
    model = aalloc.load_asset_allocation_model(book_url)
    return render_template('assetallocation.html', model=model)

@assetallocation_controller.route('/')
def asset_allocation():
    """ Asset Allocation without the securities """
    return render_template('asset_allocation.html', model=None)
