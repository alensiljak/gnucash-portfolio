"""
Asset Allocation
- display of asset allocation state
- editing of allocations (store in .json)
- manual adjustments to allocation (offset for imbalance)
"""
from logging import log, DEBUG
from flask import Blueprint, render_template #, request
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib import generic
from app.models.assetallocation_models import AssetGroupDetailsViewModel


assetallocation_controller = Blueprint( # pylint: disable=invalid-name
    'assetallocation_controller', __name__, url_prefix='/assetallocation')


@assetallocation_controller.route('/')
def asset_allocation():
    """ Asset Allocation without the securities """
    # look at AssetAllocationService in mmex.
    with BookAggregate() as svc:
        base_currency = svc.get_default_currency()

        aaloc = svc.get_asset_allocation()
        model = aaloc.load_full_model(base_currency)
        # populate actual allocation & difference.
        output = render_template('asset_allocation.html', model=model)
    return output


@assetallocation_controller.route('/settings', methods=['GET'])
def settings():
    """ Settings for Asset Allocation """
    # for now, just the primitive json editing
    content = generic.load_json_file_contents('./config/assetAllocation.json')
    model = {
        "title": "Asset Allocation settings",
        "content": content
    }
    return render_template('content.editor.html', model=model)


@assetallocation_controller.route('/settings', methods=['POST'])
def save_settings():
    """ Saves the settings content """
    return render_template('incomplete.html')


@assetallocation_controller.route('/details/<fullname>')
def details(fullname=None):
    """ Asset Class details, including the list of stocks """
    model = __get_details_model(fullname)

    return render_template('assetallocation.details.html', model=model)

def __get_details_model(fullname: str) -> AssetGroupDetailsViewModel:
    """ Creates the model for asset allocation details """
    model = AssetGroupDetailsViewModel()
    model.fullname = fullname

    with BookAggregate() as svc:
        aaloc = svc.get_asset_allocation()

        # load child classes
        # load stocks
        assetallocation = aaloc.load_config_only(None)
        log(DEBUG, assetallocation)

    return model
