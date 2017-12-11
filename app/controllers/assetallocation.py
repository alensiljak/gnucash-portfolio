"""
Asset Allocation controller
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.lib import settings, assetallocation as aalloc

assetallocation_controller = Blueprint('assetallocation_controller', __name__, url_prefix='/assetallocation')

@assetallocation_controller.route('/')
#@templated()
def assetallocation():
    """ Asset Allocation """
    book_url = settings.Settings().database_uri
    model = aalloc.load_asset_allocation_model(book_url)
    return render_template('assetallocation.html', model=model)
    #return dict(model=model)
