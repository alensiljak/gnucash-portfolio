<code>
    Price Download component for single security
</code>
<template>
  <div>
      <div class="card">
          <div class="card-header">
          </div>
          <div class="card-body form-inline">
            <div class="w-100 text-center">
              <button v-show="!price" class="btn btn-primary mx-auto" @click="fetchPrice">Fetch</button>
            </div>

            <div v-show="price" class="form-row">
              <div class="form-group">
                <label>Current Price:</label>
                <input id="currentPrice" class="form-control text-center ml-2" v-model="price" />
              </div>
              <div class="form-group ml-3">
                  <label>Currency:</label>
                  <input class="form-control text-center" readonly v-model="currency" />
              </div>
              <div class="ml-3">
                  <button class="btn btn-outline-primary" @click="importPrice">Import</button>

                  
              </div>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
import axios from "axios"
import BootstrapVue from 'bootstrap-vue'

export default {
  data() {
    return {
      symbol: "",
      currency: null,
      price: null,
      date: null,
      timezone: null
    };
  },
  props: {},

  // created: () => console.log("created"),
  mounted: function() {
    var model = window.model;

    this.symbol = model.symbol;
  },

  methods: {
    // Convert GnuCash-style symbol to Morningstar.
    getMorningstarSymbol: function(gncSymbol) {
      var parts = gncSymbol.split(":");
      var namespace = parts[0];
      var symbol = parts[1];

      var namespaceMap = {
        AMS: "XAMS",
        ASX: "XASX",
        XETRA: "XETR",
        LSE: "XLON"
      };
      namespace = namespaceMap[namespace];

      var msSymbol = namespace + ":" + symbol;
      return msSymbol;
    },
    fetchPrice: function() {
      // using Morningstar.
      var msSymbol = this.getMorningstarSymbol(this.symbol);

      axios
        .get("http://quotes.morningstar.com/stockq/c-header", {
          params: {
            t: msSymbol
          }
        })
        .then(response => {
          // test for 200?
          // console.log(response.data);

          this.price = this.parseMsHtml(response.data);
        });
    },
    parseMsHtml: function(html) {
      // get the price
      var doc = new DOMParser().parseFromString(html, "text/html");

      var priceEl = doc.getElementById("last-price-value");
      var price = priceEl.textContent.trim();

      this.date = doc.getElementById("asOfDate").textContent.trim();
      this.timezone = doc.getElementById("timezone").textContent.trim();
      this.currency = doc.getElementById("curency").textContent.trim();

      // console.log(x);

      return price;
    },
    importPrice: function() {
      axios
        .post("/price/api/create", {
          date: this.date,
          symbol: this.symbol,
          price: this.price,
          currency: this.currency
        })
        .then(function(response) {
          console.log(response.data);
        });
    }
  },

  components: {
    BootstrapVue
  }
};
</script>

<style>

</style>
