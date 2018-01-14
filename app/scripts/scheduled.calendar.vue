<!-- 
  Scheduled Transactions Calendar
  https://www.npmjs.com/package/vue-full-calendar
-->
<template>
<div>
  <!-- :events="events" -->
  <full-calendar :event-sources="eventSources" :config="config"></full-calendar>
</div>
</template>

<script>
import Vue from "vue";
import { FullCalendar } from "vue-full-calendar";
Vue.use(FullCalendar);
import axios from 'axios';

export default {
  data() {
    return {
      // events: [
      //   {
      //     title: "event1",
      //     start: "2018-01-01"
      //   },
      //   {
      //     title: "event2",
      //     start: "2018-01-05",
      //     end: "2018-01-07"
      //   },
      //   {
      //     title: "event3",
      //     start: "2018-01-09T12:30:00",
      //     allDay: false
      //   }
      // ]
      eventSources: [
        {
          events(start, end, timezone, callback) {
            axios.get("/scheduled/api/top10", { timezone: timezone }).then(response => {
              // console.log(response.data);
              callback(response.data);
            });
          },
          color: "yellow",
          textColor: "black"
        },
      ],
      config: {
        defaultView: "month",
        height: "35em",
        //aspectRatio: 4/3,
        firstDay: 1,
      }
    };
  },
  components: {
    FullCalendar
  }
};
</script>

<style>
@import "~fullcalendar/dist/fullcalendar.css";

/* color weekend */
/*.fc-fri { color:blue; }*/
.fc-sat { color:red;  }
.fc-sun { color:red;  }
</style>
 