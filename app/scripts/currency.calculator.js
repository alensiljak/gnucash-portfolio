/*
    Currency calculator
*/
import Vue from 'vue'
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue)
import App from './currency.calculator.vue'

new Vue({
  el: '#app',
  render: h => h(App)
})
