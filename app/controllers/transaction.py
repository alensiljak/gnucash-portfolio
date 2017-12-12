"""
Transactions & Splits
- account register with search (by description & memo) & filtering (date), sorting
- editing of transaction splits
- display transaction details with splits
"""
from flask import Blueprint, request, render_template
from piecash import Transaction
from gnucash_portfolio.lib.database import Database

transaction_controller = Blueprint('transaction_controller', __name__, url_prefix='/transaction')

@transaction_controller.route('/details/<tx_id>')
def tx_details(tx_id: str):
    """ Display transaction details """
    with Database().open_book() as book:
        tx = book.session.query(Transaction).filter(Transaction.guid == tx_id).one()
        #print(tx.description)
        model = {
            "transaction": tx
        }
        return render_template('transaction.details.html', model=model)
