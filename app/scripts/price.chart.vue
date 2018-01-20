<docs>
    Price chart
</docs>
<template>
<div>
    <line-chart :chart-data="chartData" :options="lineOptions" :height="chartHeight"></line-chart>
</div>
</template>

<script>
import LineChart from "./line.chart.vue";

export default {
  data() {
    return {
      chartData: null,
      lineOptions: {},
      chartHeight: 100
    };
  },
  components: {
    LineChart
  },

  mounted: function() {
    this.chartData = window.model.chartData;
  }
};
</script>

<style>

</style>
