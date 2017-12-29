/*
    Currency exchange rate download mini-app.
*/

/**
 * Represents the data model for the currency row.
 */
class Currency {
    constructor() {
        //super();
        this.symbol = undefined;
        this.rate = undefined;
        this.rateDate = undefined;
        this.saved = false;
    }
}

class CurrencyTableRow extends React.Component {
    constructor(prop) {
        super(prop);
        this.state = {
            currency: prop.currency
        };
    }
    render() {
        return (

            <tr key={this.state.currency.symbol}>
                <td>
                    {this.state.currency.symbol}
                </td>
                <td>{this.state.currency.rate}</td>
                <td>
                    {this.state.currency.rateDate}
                </td>
                <td>{this.state.currency.saved}</td>
            </tr>

        );
    }
}

/**
 * Currency rate table. 
 * Displays the book currencies and the downloaded rates.
 */
class CurrencyTable extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currencies: props.currencies
        };
    }

    render() {
        return (
            <table className="table table-bordered table-striped">
                <thead className="thead-dark">
                    <tr>
                        <th>Currency</th>
                        <th>Value</th>
                        <th>Date</th>
                        <th>Saved</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.currencies.map((currency, i) =>
                        <CurrencyTableRow key={currency.symbol} currency={currency} />
                    )}
                </tbody>
            </table>
        )
    }
}

class Main extends React.Component {
    constructor(props) {
        super(props);

        var currencies = this.initCurrencies(props.currencies);
        this.state = {
            currencies: currencies,
            importEnabled: false,
            response: undefined     // response from the rates server.
        };
    }

    /**
     * Initialize the list of Currency objects from the list of symbols received from the page.
     */
    initCurrencies = function (symbols) {
        var currencies = [];
        // console.log("received", symbols.length, "symbols.");

        for (var i = 0; i < symbols.length; i++) {
            var symbol = symbols[i];
            // console.log("creating", symbol);
            var currency = new Currency();
            currency.symbol = symbol;

            currencies.push(currency);
        }

        // console.log(currencies);
        return currencies;
    }

    downloadAll = function (event) {
        // Just get all and then parse the result
        // console.log("fetching rates...");
        var that = this;
        $.ajax({
            url: 'https://api.fixer.io/latest',
            method: 'GET',
            success: function (data) {
                // console.log("received:", data);
                that.displayRates(data);
                that.enableImport();
            }
        });
    };

    enableImport = function () {
        this.setState({ importEnabled: true });
    }

    /**
     * Stores and displays the information received from the rates server.
     */
    displayRates = function (rates_result) {
        // Populate rows by updating the collection.
        var rates_dict = rates_result.rates;
        var currencies = this.state.currencies;

        for (var i = 0; i < currencies.length; i++) {
            var cur = currencies[i];
            var rate = rates_dict[cur.symbol];
            // console.log("assigning", rate, "to", cur.symbol);
            cur.rate = rate;
            cur.rateDate = rates_result.date;
        }
        this.setState({ currencies: currencies });
    }

    importAll = function () {
        // console.log("Here goes import");
        $.ajax({
            url: '/currency/api/saverates',
            method: 'POST',
            data: { 
                currencies: JSON.stringify(this.state.currencies),
                base: this.state.response.base
            },
            success: function (data) {
                console.log("server response:", data);
            }
        });
    }

    render() {
        return (
            <div>
                <h2>Book currencies</h2>
                <CurrencyTable currencies={this.state.currencies} />
                <div className="text-center">
                    <button className="btn btn-primary" onClick={event => this.downloadAll(event)}>
                        Download all
                    </button>
                    {this.state.importEnabled ?
                        <button className="btn btn-outline-primary ml-3" onClick={event => this.importAll(event)}>
                            Import all
                    </button>
                        : null}
                </div>
            </div>
        );
    }
}
