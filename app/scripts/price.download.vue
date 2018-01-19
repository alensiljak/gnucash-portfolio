<code>
    Price Download component for single security
</code>
<template>
  <div>
      <div class="card">
          <div class="card-header">
          </div>
          <div class="card-body">
              <button class="btn" @click="fetchPrice">Fetch</button>
          </div>
      </div>
  </div>
</template>

{{ test }}

<script>
import axios from "axios"

export default {
    data() {
        return {
            symbol: ""
        }
    },
    props: {
    },

    // created: () => console.log("created"),
    mounted: function() {
        this.symbol = window.model.symbol
    },

    methods: {
        fetchPrice: function() {
            axios.get('/')
                .then(function(response) {
                    // test for 200?
                    console.log(response.data)
                })
        }
    }
}
</script>

<style>

</style>
