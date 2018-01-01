<docs>
Currency table row component.
</docs>

<template>
    <tr key={{currency.symbol}}>
        <td>{{currency.symbol}}</td>
        <td class="text-right">{{currency.rate}}</td>
        <td class="text-right">{{currency.inverseRate}}</td>
        <td>{{currency.rateDate}}</td>
        <td>{{currency.saved}}</td>
    </tr>
</template>
<script>
export default {
  data() {
    return {
    //   msg: "Hello world!"
    };
  },
  props: ['currency']
};
</script>
