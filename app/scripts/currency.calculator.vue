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
                  <label for="sourceCurrency" class="mr-2">Currency symbol</label>
                  <select name="sourceCurrency" class="form-control chosen">
                      <option v-for="currency in currencies">{{ currencies[currency] }}</option>
                  </select>
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
              <ul>
                <li v-for="currency in Object.keys(currencies)">{{ currency }} ({{ currencies[currency] }})</li>
              </ul>
            </div>
          </div>
      </div>
  </div>
</div>

</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      currencies: [],
      srcCurrency: null,
      dstCurrency: null
    };
  },
  props: {

  },
  methods: {

    },
  mounted: function mounted() {
    $("#amount").focus();

    // load currencies
    axios.get('/currency/api/rates')
      .then(response => {
        // console.log(response.data);
        console.log("rates fetched");
        this.currencies = response.data;
      })
      .catch(error => {
        console.error(error);
      });

    // $.ajax({
    //   url: '/currency/api/rates',
    //   success: function(data) {
    //     // console.log(data);
    //     // for (var key in data) {
    //     //   if (data.hasOwnProperty(key)) {
    //     //     currencies.push(data[key])
    //     //   }
    //     // }
    //     that.currencies = data;
    //   }
    // });
  }
};
</script>
<style>
</style>