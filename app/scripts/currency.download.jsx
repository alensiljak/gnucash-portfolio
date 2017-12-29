class CurrencyTable extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currencies: props.currencies
        }
    }

    render() {
        return (
            <table className="table table-bordered table-striped">
                <thead></thead>
                <tbody>
                    {this.state.currencies.map(currency =>
                        <tr>
                            <td>
                                {currency}
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        )
    }
}

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currencies: props.currencies
        }
    }
    render() {
        return (
            <div>
                <h1>Hello, world!</h1>
                <CurrencyTable currencies={this.state.currencies} />
            </div>
        );
    }
}
