<docs>
Currency download page, implemented in vue.js.
</docs>

<template>
    <table class="table table-bordered table-striped">
        <thead class="thead-dark">
            <tr>
                <th>Currency</th>
                <th>Value</th>
                <th>Date</th>
                <th>Saved</th>
            </tr>
        </thead>
        <tbody>
            <CurrencyTableRow v-for="currency in currencies" :key="currency.symbol" v-bind:currency="currency" />
        </tbody>
    </table>
</template>
<script>
import CurrencyTableRow from './currency.download.table.row.vue'

export default {
  data() {
    return {
    //   msg: "Hello world!"
    };
  },
  props: ['currencies'],
  components: {
      CurrencyTableRow
  }
};
</script>
