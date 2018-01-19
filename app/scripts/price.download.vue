<code>
    Price Download component for single security
</code>
<template>
  <div>
      <div class="card">
          <div class="card-header">
          </div>
          <div class="card-body">
              <button v-show="!price" class="btn" @click="fetchPrice">Fetch</button>

            <div v-show="price">
              <div class="form-group">
                  <label>Current Price:</label>
              <input id="currentPrice" class="form-control" v-model="price" />
              </div>

              <div>
                  todo: select currency
                  {{ currency }}
              </div>
              <div>
                  todo: import (send the values to an api endpoint)
              </div>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      symbol: "",
      currency: null,
      price: null
    };
  },
  props: {},

  // created: () => console.log("created"),
  mounted: function() {
    var model = window.model;

    this.symbol = model.symbol;
    this.currency = model.currency;
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
          this.price = this.parseMsHtml(response.data);
        });
    },
    parseMsHtml: function(html) {
      // todo: get the price
      var doc = new DOMParser().parseFromString(html, "text/html");
      var priceEl = doc.getElementById("last-price-value");
      var price = priceEl.textContent.trim();

      console.log(price);

      return price;
    }
  }
};
</script>

<style>

</style>
