<!-- Securities main page -->
<template>
  <div>
    <p>Test Vue autocomplete</p>

    <type-ahead src="/security/api/search?query=:keyword" :value="symbol" :getResponse="getResponse"
        :placeholder="placeholder" />
  </div>
</template>

<script>
import TypeAhead from "vue2-typeahead";

export default {
  data() {
    return {
        "symbol": "",
        "placeholder": "type symbol to search securities"
    };
  },

  components: {
    TypeAhead
  },

  methods: {
    getResponse: function(data) {
      return data;
    }
  }
};
</script>

<style>

</style>
