<!-- Securities main page -->
<template>
  <div>
    <p>Test Vue autocomplete</p>

    <v-select
        class="form-control"
        :debounce="250"
        :on-search="getOptions"
        :options="options"
        placeholder="Search account..."
        label="value"
    ></v-select>
  </div>
</template>

<script>
import vSelect from "vue-select"
import axios from "axios"

export default {
  data() {
    return {
        "symbol": "",
        "placeholder": "type symbol to search securities",
        options: []
    };
  },

  components: {
    vSelect
  },

  methods: {
    getOptions: function(search, loading) {
        if (search.length < 2) return;

        loading(true)

      axios.get("/security/api/search", {
          params: {
              query: search
          }
      }).then(response => {
        // TODO: store into model.
        this.options = response.data.suggestions
        // var result = response.data.suggestions.map(x => x.value);
        loading(false)
      });
    }
  }
};
</script>

<style>

</style>
