<docs>
Currency calculator
</docs>

<template>
<div>
    <div class="card">
        <div class="card-header">
            FX Calculator
        </div>
        <div class="card-body">
            <div class="row">

                <div class="col">
                    <div class="form-group">
                        <label for="srcCurrency" class="mr-2">Source Currency</label>
                        <model-select :options="listModel" v-model="srcCurrency" placeholder="source currency" @input="onSelect">
                        </model-select>
                        <b-alert variant="warning" :show="alertSrcCurrency">Currency not selected</b-alert>
                    </div>
                </div>
                <div class="col-1 my-auto">
                  <button class="btn btn-dark text-light" @click="swap">
                    <i class="fa fa-exchange"></i>
                  </button>
                </div>
                <div class="col">
                    <div class="form-group">
                        <label for="srcCurrency" class="mr-2">Destination Currency</label>
                        <model-select :options="listModel" v-model="dstCurrency" placeholder="destination currency" @input="onSelect">
                        </model-select>
                        <b-alert variant="warning" :show="alertDstCurrency">Currency not selected</b-alert>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                  <!-- Amount -->
                    <div class="form-group">
                        <label>Amount</label>
                        <input id="amount" class="form-control text-right" v-model.number="amount" @change="onSelect" @focus="$event.target.select()">
                    </div>
                </div>

                <div class="col">
                    <!-- Result -->
                    <div class="form-group">
                        <label>Result</label>
                        <input id="result" readonly="readonly" class="form-control text-right" v-model="result">
                    </div>
                </div>
            </div>

            <div class="row mt-2">
                <div class="mx-auto">
                    <button class="btn btn-primary" @click="recalculate">Calculate</button>
                </div>
            </div>
        </div>
    </div>

    <a href="#" @click="use('EUR','USD')">EUR-USD</a>
    &bullet;
    <a href="#" @click="use('EUR','AUD')">EUR-AUD</a>
</div>

</template>
<script>
import axios from "axios";
import { ModelSelect } from "vue-search-select";

export default {
  data() {
    return {
      currencies: {},
      listModel: [],
      srcCurrency: {
        value: "",
        text: ""
      },
      dstCurrency: {
        value: "",
        text: ""
      },
      amount: 0,
      amountInBase: 0, // Amount in base currency
      result: 0,
      //alerts
      alertSrcCurrency: false,
      alertDstCurrency: false
    };
  },
  props: {},
  methods: {
    onSelect: function(item) {
      this.recalculate();
    },
    recalculate: function() {
      console.debug("recalculating...", this.amount, this.srcCurrency.text, "into", this.dstCurrency.text);

      this.alertSrcCurrency = !this.srcCurrency.text;
      this.alertDstCurrency = !this.dstCurrency.text;

      if (!this.amount || !this.srcCurrency.text || !this.dstCurrency.text) {
        // console.log("input missing. Exiting.")
        return;
      }

      // get source
      // console.log(JSON.stringify(this.srcCurrency));
      if (this.srcCurrency.text === "EUR") {
        // already base currency
        this.amountInBase = this.amount;
      } else {
        // recalculate to base currency
        this.amountInBase = this.amount * this.srcCurrency.value;
      }

      // calculate destination
      // handle 0 values
      if (!this.dstCurrency.value) {
        this.dstCurrency.value = 1
      }
      this.result = this.amountInBase / this.dstCurrency.value;
      // round to 2 decimals
      this.result = Math.round(this.result * 100) / 100;

      // recalculate
      // console.log("recalculation complete");
    },
    swap: function() {
      // swap the currencies
      var temp = this.dstCurrency
      this.dstCurrency = this.srcCurrency
      this.srcCurrency = temp

      this.recalculate()
    },
    use: function(src, dst) {
      // console.log(src, dst)
      this.srcCurrency = {
        value: this.currencies[src],
        text: src
      };
      this.dstCurrency = {
        value: this.currencies[dst],
        text: dst
      };
      this.recalculate();
    }
  },
  mounted: function mounted() {
    // Initialization.
    var self = this;

    $("#amount").focus();

    // load currencies
    axios
      .get("/currency/api/rates")
      .then(function(response) {
        console.log("rates fetched");
        self.currencies = response.data;

        for (var symbol in response.data) {
          // console.log("adding", index, response.data[symbol]);
          self.listModel.push({ text: symbol, value: response.data[symbol] });
        }

        // refresh the selectors
        $("#srcCurrency").trigger("chosen:updated");
        // $('#srcCurrency').chosen();
      })
      .catch(function(error) {
        console.error(error);
      });
  },
  components: {
    ModelSelect
  }
};
</script>
<style>

</style>
