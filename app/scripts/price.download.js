/**
 * Price download functionality for a single security.
 * Uses the price download component.
 */
import Vue from 'vue'
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue)
import App from './price.download.vue'

new Vue({
    el: '#app',
    render: h => h(App)
})
