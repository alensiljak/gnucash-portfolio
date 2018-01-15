/**
 * Account Transactions Vue app.
 */
import Vue from 'vue'
import App from './account.transactions.vue'
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  render: h => h(App)
})
