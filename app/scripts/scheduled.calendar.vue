<!-- 
  Scheduled Transactions Calendar
-->
<template>
<div>
  <p>Calendar</p>
  <full-calendar :events="events"></full-calendar>
</div>
</template>

<script>
import Vue from "vue";
import { FullCalendar } from "vue-full-calendar";
Vue.use(FullCalendar);

export default {
  data() {
    return {
      events: [
        {
          title: "event1",
          start: "2010-01-01"
        },
        {
          title: "event2",
          start: "2010-01-05",
          end: "2010-01-07"
        },
        {
          title: "event3",
          start: "2010-01-09T12:30:00",
          allDay: false
        }
      ]
    };
  },
  components: {
    FullCalendar
  }
};
</script>

<style>
@import "~fullcalendar/dist/fullcalendar.css";
</style>
 