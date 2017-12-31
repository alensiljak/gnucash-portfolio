<docs>
Currency download page, implemented in vue.js.
</docs>

<template>
    <div>
        <h3>Book currencies</h3>
        <CurrencyTable currencies={this.currencies} />
        <div className="text-center">
            <button className="btn btn-primary" @click="downloadAll">
                Download all
            </button>
            {this.state.importEnabled ?
                <button className="btn btn-outline-primary ml-3" @click="importAll">
                    Import all
            </button>
                : null}
        </div>
    </div>
</template>
<script>
import CurrencyTable from "./currency.download.table.vue";

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

export default {
  data() {
    return {
      currencies: []
    };
  },
//   props: ['currencies'],
  methods: {
    downloadAll: function(event) {
      // Just get all and then parse the result
      // console.log("fetching rates...");
      var that = this;
      $.ajax({
        url: "https://api.fixer.io/latest",
        method: "GET",
        success: function(data) {
          // console.log("received:", data);
          that.displayRates(data);
          that.enableImport();
        }
      });
    },
    get_book_currencies: function() {
        var that = this;

        $.ajax({
            url: '/currency/api/book_currencies',
            success: function(data) {
                // console.log(data);
                that.initCurrencies(data);
            }
        })
    },
    importAll: function() {
      // Send the rates to GnuCash Portfolio.

      // clear the output first.
      this.setSaved(false);

      var that = this;
      $.ajax({
        url: "/currency/api/saverates",
        method: "POST",
        data: {
          currencies: JSON.stringify(this.state.currencies),
          base: this.state.response.base,
          date: this.state.response.date
        },
        success: function(data) {
          var saved = false;
          if (data == "true") {
            saved = true;
          }

          // Display result
          that.setSaved(saved);
        }
      });
    },
    /**
     * Initialize the list of Currency objects from the list of symbols received from the page.
     */
    initCurrencies: function (symbols) {
        // console.log("got", symbols);

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
        // return currencies;
        this.currencies = currencies;
    }
  },
  mounted: function() {
    // `this` points to the vm instance
    // console.log('a is: ' + this.a)
    console.log("Initializing currencies...");
    this.get_book_currencies()
  },
  components: {
    CurrencyTable
  }
};
</script>
