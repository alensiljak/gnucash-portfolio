<code>
    Price Download component for single security
</code>
<template>
  <div>
      <div class="card">
          <div class="card-header">
          </div>
          <div class="card-body">
              <button class="btn" @click="fetchPrice">Fetch</button>

            <div v-show="price">
              <div class="form-group">
                  <label>Current Price:</label>
              <input id="currentPrice" class="form-control" v-model="price" />
              </div>

              <div>
                  todo: select currency
              </div>
              <div>
                  todo: import (send the values to an api endpoint)
              </div>
            </div>
          </div>
      </div>
  </div>
</template>

{{ test }}

<script>
import axios from "axios";

export default {
  data() {
    return {
      symbol: "",
      price: null
    };
  },
  props: {},

  // created: () => console.log("created"),
  mounted: function() {
    this.symbol = window.model.symbol;
  },

  methods: {
    fetchPrice: function() {
      // using Morningstar.

      axios.get("/").then(response => {
        // test for 200?
        this.price = this.parseMsHtml(response.data);
      });
    },
    parseMsHtml: function(html) {
      // todo: get the price
      return html;
    }
  }
};
</script>

<style>

</style>
