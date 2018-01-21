/**
 * Dashboard
 */
import Vue from 'vue'

// Tiny scheduled transactions calendar
import TinyCal from './scheduled.calendar.tiny.vue'

new Vue({
  el: '#tinyCalendar',
  render: h => h(TinyCal)
})
