"""
Asset Allocation
- display of asset allocation state
- editing of allocations (store in .json)
- manual adjustments to allocation (offset for imbalance)
"""
from decimal import Decimal
#from logging import log, DEBUG
from flask import Blueprint, render_template #, request
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.lib import generic
from app.models.assetallocation_models import (AssetGroupDetailsViewModel,
                                               AssetGroupChildDetailViewModel)

assetallocation_controller = Blueprint( # pylint: disable=invalid-name
    'assetallocation_controller', __name__, url_prefix='/assetallocation')

@assetallocation_controller.route('/')
def asset_allocation():
    """ Asset Allocation without the securities """
    # look at AssetAllocationService in mmex.
    with BookAggregate() as svc:
        base_currency = svc.currencies.get_default_currency()

        aaloc = svc.asset_allocation
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

@assetallocation_controller.route('/details/<path:fullname>')
def details(fullname=None):
    """ Asset Class details, including the list of stocks """
    model = __get_details_model(fullname)

    return render_template('assetallocation.details.html', model=model)

#########################
# Private

def __get_details_model(fullname: str) -> AssetGroupDetailsViewModel:
    """ Creates the model for asset allocation details """
    model = AssetGroupDetailsViewModel()
    model.fullname = fullname

    with BookAggregate() as svc:
        model.base_currency = svc.currencies.get_default_currency().mnemonic

        aaloc = svc.asset_allocation
        # Load only the asset class tree without the data from database.
        aaloc.root = aaloc.load_config_only(None)
        asset_class = aaloc.find_class_by_fullname(fullname)

        model.asset_class = asset_class

        # Load value of each security.
        if hasattr(asset_class, "classes"):
            for ac in asset_class.classes:
                child = AssetGroupChildDetailViewModel()
                child.name = ac.name
                child.fullname = ac.fullname
                child.value = Decimal(0)
                model.classes.append(child)

        if hasattr(asset_class, "stocks"):
            for stock in asset_class.stocks:
                sec = svc.securities.get_aggregate_for_symbol(stock.symbol)

                child = AssetGroupChildDetailViewModel()
                child.fullname = stock.symbol
                child.name = stock.symbol
                child.description = sec.security.fullname
                child.quantity = sec.get_quantity()
                child.value = sec.get_value()
                child.currency = sec.get_currency().mnemonic
                child.value_base_cur = sec.get_value_in_base_currency()

                model.stocks.append(child)

    return model
