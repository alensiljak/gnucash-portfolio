<template>
<div>
    <!-- Tiny version of the scheduled transactions calendar. -->
    <full-calendar :event-sources="eventSources" :config="config"></full-calendar>
</div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import { FullCalendar } from "vue-full-calendar";
Vue.use(FullCalendar);

export default {
  data() {
    return {
      eventSources: [
        {
          events(start, end, timezone, callback) {
            axios
              .get("/scheduled/api/transactions/20", { timezone: timezone })
              .then(response => {
                // console.log(response.data);
                callback(response.data);
              });
          },
          color: "yellow",
          textColor: "black"
        }
      ],
      config: {
        defaultView: "month",
        height: 310,
        //aspectRatio: 4/3,
        firstDay: 1,
        header: {
          left: "prev,next today",
          center: "title",
          right: "month" //,agendaWeek,agendaDay"
        },
        eventLimit: true, // allow "more" link when too many events

        eventAfterRender: function() {
          // add titles to "+# more links"
          $(".fc-more-cell a").each(function() {
            this.title = this.textContent;
          });
        },

        // add event name to title attribute on mouseover
        eventMouseover: function(event, jsEvent, view) {
          console.log(event.target);

          if (view.name !== "agendaDay") {
            $(jsEvent.target).attr("title", event.title);
          }
        }
      }
    };
  },
  mounted: function() {},
  components: {
    FullCalendar
  }
};
</script>

<style>
@import "~fullcalendar/dist/fullcalendar.css";

#calendar {
  width: 200px;
  margin: 0 auto;
  font-size: 10px;
}
.fc-toolbar {
  font-size: 0.9em;
}
.fc-toolbar h2 {
  font-size: 12px;
  white-space: normal !important;
}
/* click +2 more for popup */
.fc-more-cell a {
  display: block;
  width: 85%;
  margin: 1px auto 0 auto;
  border-radius: 3px;
  background: grey;
  color: transparent;
  overflow: hidden;
  height: 4px;
}
.fc-more-popover {
  width: 100px;
}
.fc-view-month .fc-event,
.fc-view-agendaWeek .fc-event,
.fc-content {
  font-size: 0;
  overflow: hidden;
  height: 2px;
}
.fc-view-agendaWeek .fc-event-vert {
  font-size: 0;
  overflow: hidden;
  width: 2px !important;
}
.fc-agenda-axis {
  width: 20px !important;
  font-size: 0.7em;
}

.fc-button-content {
  padding: 0;
}
</style>
