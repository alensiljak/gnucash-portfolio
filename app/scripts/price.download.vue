<code>
    Price Download component for single security
</code>
<template>
  <div>
      <div class="card">
          <div class="card-header">
          </div>
          <div class="card-body form-inline">
            <div class="w-100 text-center" v-show="!price">
              <button class="btn btn-primary mx-auto" @click="fetchPrice">Fetch</button>
            </div>

            <div v-show="price" class="form-row">
              <div class="form-group">
                <label>Current Price:</label>
                <input id="currentPrice" class="form-control text-center ml-2" readonly :value="price" />
              </div>
              <div class="form-group ml-3">
                  <label>Date:</label>
                  <input class="form-control text-center ml-2" readonly :value="date" />
              </div>
              <div class="form-group ml-3">
                  <label>Currency:</label>
                  <input class="form-control text-center ml-2" readonly :value="currency" />
              </div>
            </div>

            <div v-show="price" class="form-row w-100 mt-3">
              <div class="form-group ml-3 mx-auto" v-show="!imported">
                  <button class="btn btn-outline-primary" @click="importPrice">Import</button>
              </div>
              <div class="form-group ml-3 mx-auto">
                  <b-alert class="my-auto" variant="danger" :show="alertNotImported">✗ Not imported</b-alert>
                  <b-alert class="my-auto" variant="success" :show="alertImported">✓ Imported</b-alert>
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
      price: null,
      date: null,
      timezone: null,
      // indicators
      imported: false,
      // alerts
      alertImported: false,
      alertNotImported: false
    };
  },
  props: {},

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
      window.document.body.style.cursor = "wait"

      var msSymbol = this.getMorningstarSymbol(this.symbol);

      axios
        .get("http://quotes.morningstar.com/stockq/c-header", {
          params: {
            t: msSymbol
          }
        })
        .then(response => {
          // test for 200?
          // console.log(response)

          this.parseMsHtml(response.data);
          window.document.body.style.cursor = "default"
        });
    },
    parseMsHtml: function(html) {
      // get the price
      if (!html) return;
      var doc = new DOMParser().parseFromString(html, "text/html");

      var priceEl = doc.getElementById("last-price-value");
      if (!priceEl) {
        console.warn("No price information found in", html)
        return;
      }
      var price = priceEl.textContent.trim();

      this.date = doc.getElementById("asOfDate").textContent.trim();
      this.timezone = doc.getElementById("timezone").textContent.trim();
      this.currency = doc.getElementById("curency").textContent.trim();

      // console.log(x);

      return price;
    },
    importPrice: function() {
      window.document.body.style.cursor = "wait"

      axios
        .post("/price/api/create", {
          date: this.date,
          symbol: this.symbol,
          price: this.price,
          currency: this.currency
        })
        .then(response => {
          // console.log(response.data);
          var result = response.data;
          if (result.success) {
            this.alertImported = true;
            this.imported = true;
          } else {
            this.alertNotImported = true;
          }

          window.document.body.style.cursor = "default"
        });
    }
  },

  components: {}
};
</script>

<style>

</style>
