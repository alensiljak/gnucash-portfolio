<!-- 
  Scheduled Transactions Calendar
  https://www.npmjs.com/package/vue-full-calendar
  For tiny version, see
  https://stackoverflow.com/questions/5372328/tiny-version-of-fullcalendar
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
      eventSources: [
        {
          events(start, end, timezone, callback) {
            axios.get("/scheduled/api/transactions/30", { timezone: timezone }).then(response => {
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
      },
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
 