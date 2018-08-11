""" Security Info report
Returns a model that can be used in any visualizer.
"""

from gnucash_portfolio import BookAggregate
from gnucash_portfolio.model.stock_model import SecurityDetailsViewModel


class SecurityInfoReport:
    """ Security Info report model """
    def __init__(self, svc: BookAggregate):
        self._svc = svc

    def run(self, symbol: str) -> SecurityDetailsViewModel:
        """ Loads the model for security details """
        svc = self._svc
        sec_agg = svc.securities.get_aggregate_for_symbol(symbol)

        model = SecurityDetailsViewModel()

        model.symbol = sec_agg.security.namespace + ":" + sec_agg.security.mnemonic
        model.security = sec_agg.security

        # Quantity
        model.quantity = sec_agg.get_quantity()
        model.value = sec_agg.get_value()
        currency = sec_agg.get_currency()
        if currency:
            assert isinstance(currency, str)
            model.currency = currency
        model.price = sec_agg.get_last_available_price()

        model.average_price = sec_agg.get_avg_price()
        # Here we take only the amount paid for the remaining stock.
        model.total_paid = sec_agg.get_total_paid_for_remaining_stock()

        # Profit/loss
        model.profit_loss = model.value - model.total_paid
        if model.total_paid:
            model.profit_loss_perc = abs(model.profit_loss) * 100 / model.total_paid
        else:
            model.profit_loss_perc = 0
        if abs(model.value) < abs(model.total_paid):
            model.profit_loss_perc *= -1
        # Income
        model.income = sec_agg.get_income_total()
        if model.total_paid:
            model.income_perc = model.income * 100 / model.total_paid
        else:
            model.income_perc = 0
        # income in the last 12 months
        # income_last_year = sec_agg.get_income_total
        # model.income_perc_last_12m = 0

        # Return of Capital
        roc = sec_agg.get_return_of_capital()
        model.return_of_capital = roc

        # total return
        model.total_return = model.profit_loss + model.income
        if model.total_paid:
            model.total_return_perc = model.total_return * 100 / model.total_paid
        else:
            model.total_return_perc = 0

        # load all accounts
        model.accounts = sec_agg.accounts
        model.income_accounts = sec_agg.get_income_accounts()

        # Load asset classes to which this security belongs.
        # todo load asset allocation, find the parents for this symbol
        # svc.asset_allocation.load_config_only(svc.currencies.default_currency)
        # stocks = svc.asset_allocation.get_stock(model.symbol)
        #
        # for stock in stocks:
        #     model.asset_classes.append(stock.asset_class)
        from asset_allocation import AppAggregate
        aa = AppAggregate()
        aa.open_session()
        aa.get_asset_classes_for_security(None, model.symbol)

        return model
