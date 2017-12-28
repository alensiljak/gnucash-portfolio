"""
Transactions & Splits
- account register with search (by description & memo) & filtering (date), sorting
- editing of transaction splits
- display transaction details with splits
"""
from flask import Blueprint, request, render_template
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.transactionaggregate import TransactionsAggregate

transaction_controller = Blueprint( # pylint: disable=invalid-name
    'transaction_controller', __name__, url_prefix='/transaction')

@transaction_controller.route('/details/<tx_id>')
def tx_details(tx_id: str):
    """ Display transaction details """
    with BookAggregate() as svc:
        tx_svc = TransactionsAggregate(svc.book)
        tran = tx_svc.get(tx_id)

        model = {
            "transaction": tran
        }
        return render_template('transaction.details.html', model=model)
