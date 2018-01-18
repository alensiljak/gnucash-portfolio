<!-- Securities main page -->
<template>
  <div>

<div class="card bg-secondary text-dark">
    <div class="card-body">

    <form ref="form" class="form">
    <v-select
      v-model="security"
        class="form-control"
        :debounce="250"
        :on-search="getOptions"
        :options="options"
        placeholder="Search securities..."
        label="value"
        @input="securityChanged"
        name="search.symbol"
        v-focus
    ></v-select>
    </form>
  </div>
</div>

<div class="mt-3" />

  <a href="/security/list" class="btn btn-outline-primary">show all</a>

  </div>
</template>

<script>
import vSelect from "vue-select";
import axios from "axios";
// import { focus } from 'vue-focus';

const focus = {
  inserted(el) {
    el.querySelector("input").focus();
  }
};

export default {
  directives: { focus: focus },

  data() {
    return {
      security: null,
      options: []
    };
  },

  components: {
    vSelect
  },

  methods: {
    getOptions: function(search, loading) {
      if (search.length < 2) return;

      loading(true);

      axios
        .get("/security/api/search", {
          params: {
            query: search
          }
        })
        .then(response => {
          // TODO: store into model.
          this.options = response.data.suggestions;
          // var result = response.data.suggestions.map(x => x.value);
          loading(false);
        });
    },
    securityChanged: function(security) {
      if (!security) return;

      // :on-change="securityChanged"
      // console.log(security.data);
      // this.$refs.form.submit();
      window.location = "/security/details/" + security.data;
    }
  }
};
</script>

<style>

</style>
