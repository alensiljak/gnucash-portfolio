<docs>
    Price chart
</docs>
<template>
<div>
    <line-chart :data="lineData" :options="lineOptions"></line-chart>
</div>
</template>

<script>
import LineChart from "./line.chart.vue";

export default {
    data() {
        return {
            lineData: [10, 20, 30],
            lineOptions: {}
        }
    },
  components: {
    LineChart
  }
};
</script>

<style>

</style>
