<docs>
Currency download page, implemented in vue.js.
</docs>

<template>
    <div>
        <h3>Book currencies</h3>
        <CurrencyTable v-bind:currencies="currencies" />
        <div className="text-center">
            <button class="btn btn-primary" @click="downloadAll">
                Download all
            </button>
            <button v-if="importEnabled" class="btn btn-outline-primary ml-3" @click="importAll">
                Import all
            </button>
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
      currencies: [],
      // Response from the server when getting the rates from rates provider.
      response: null,
      importEnabled: false
    };
  },
  //   props: ['currencies'],
  methods: {
    /**
     * Stores and displays the information received from the rates server.
     */
    displayRates: function(rates_result) {
      // Populate rows by updating the collection.
      this.response = rates_result;
      var rates_dict = rates_result.rates;

      for (var i = 0; i < this.currencies.length; i++) {
        var cur = this.currencies[i];
        var rate = rates_dict[cur.symbol];
        // console.log("assigning", rate, "to", cur.symbol);
        cur.rate = rate;
        cur.rateDate = rates_result.date;
      }
    },

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

    enableImport: function() {
      this.importEnabled = true;
    },

    get_book_currencies: function() {
      var that = this;

      $.ajax({
        url: "/currency/api/book_currencies",
        success: function(data) {
          that.initCurrencies(data);
        }
      });
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
          currencies: JSON.stringify(this.currencies),
          base: this.response.base,
          date: this.response.date
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
    initCurrencies: function(symbolsString) {
      var symbols = JSON.parse(symbolsString);
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
    },

    setSaved: function(value) {
      // Set all currency 'saved' indicators to the given value.

      for (var i = 0; i < this.currencies.length; i++) {
        this.currencies[i].saved = value;
      }
    }
  },
  mounted: function() {
    // `this` points to the vm instance
    // console.log('a is: ' + this.a)
    console.log("Initializing currencies...");
    this.get_book_currencies();
  },
  components: {
    CurrencyTable
  }
};
</script>
