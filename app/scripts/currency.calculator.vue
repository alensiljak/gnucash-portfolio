<docs>
Currency calculator
</docs>

<template>

<div>
  <div class="row w-100">
      <div class="form-group mx-auto">
          <label>Amount</label>
          <input id="amount" class="form-control text-right">
      </div>
  </div>
  <div class="row">
      <div class="col">
          <div class="card">
            <div class="card-header">
              Source Currency
            </div>
            <div class="card-body">
              <div class="form-group">
                <label for="srcCurrency" class="mr-2">Currency symbol</label>
                <model-select :options="listModel"
                                v-model="srcCurrency"
                                placeholder="select item"
                                @select="onSelect">
                </model-select>
              </div>
            </div>
          </div>
      </div>
      <div class="col">
          <div class="card">
            <div class="card-header">
              Destination Currency
            </div>
            <div class="card-body">
              <div class="form-group">
                <label for="srcCurrency" class="mr-2">Currency symbol</label>
                <model-select :options="listModel"
                                v-model="dstCurrency"
                                placeholder="select item"
                                @select="onSelect">
                </model-select>
              </div>
            </div>
          </div>
      </div>
  </div>
</div>

</template>
<script>
import axios from 'axios'
import { ModelSelect } from 'vue-search-select'

export default {
  data() {
    return {
      currencies: {},
      listModel: [],
      srcCurrency: {
        value: '',
        text: ''
      },
      dstCurrency: {
        value: '',
        text: ''
      }
    };
  },
  props: {

  },
  methods: {
    onSelect: function(item) {
      // TODO: recalculate the amount
    },
    recalculate: function() {
      // get source
      // get destination
      // recalculate?
      // should this be a server-side operation?
    }
  },
  mounted: function mounted() {
    // Initialization.
    var self = this;

    $("#amount").focus();

    // load currencies
    axios.get('/currency/api/rates')
      .then(function(response) {
        console.log("rates fetched");
        self.currencies = response.data;

        for (var symbol in response.data) {
          // console.log("adding", index, response.data[symbol]);
          self.listModel.push({ text: symbol, value: response.data[symbol] });
        }

        // refresh the selectors
        $('#srcCurrency').trigger("chosen:updated");
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