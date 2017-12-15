"""
Asset Allocation
- display of asset allocation state
- editing of allocations (store in .json)
- manual adjustments to allocation (offset for imbalance)
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio import Database
from gnucash_portfolio.assetallocation import AllocationLoader
from gnucash_portfolio.lib.settings import Settings
from gnucash_portfolio.bookaggregate import BookAggregate

assetallocation_controller = Blueprint('assetallocation_controller', __name__, url_prefix='/assetallocation')


@assetallocation_controller.route('/')
def asset_allocation():
    """ Asset Allocation without the securities """
    with BookAggregate() as book:
        base_currency = book.get_default_currency()

        loader = AllocationLoader(base_currency.mnemonic)
        model = loader.load_asset_allocation_model(book.book)
        output = render_template('asset_allocation.html', model=model)
    return output
