/**
    Account transactions
    - Incomplete! -
 */
<template>
<div>
<div class="card bg-secondary text-dark">
    <div class="card-header"></div>
    <div class="card-body">
        <form action="/account/transactions" method="POST" class="form">
            <div class="row">
                <!-- Account -->
                <div class="form-group col-md">
                    <!-- <label for="account">Account</label> -->
                    <v-select
                        class="form-control"
                        :debounce="250"
                        :on-search="getOptions"
                        :options="options"
                        placeholder="Search account..."
                        label="value"
                    ></v-select>
                </div>

                <!-- Date Period -->
                <div class="form-group col-md">
                    <!-- <label for="period">Period</label> -->
                    <date-picker lang="en" name="dateFrom" placeholder="Date from" v-model="dateFrom" /> - 
                    <date-picker lang="en" name="dateTo" placeholder="Date to" v-model="dateTo" />
                </div>
            </div>
            <div class="form-row">
                <div class="text-center col-md">
                    <button id="submit" class="btn btn-primary">Apply</button>
                </div>
            </div>
        </form>
    </div>
</div>

<p>
    Starting balance: model.start_balance, Ending balance: model.end_balance
</p>

<table class="table table-sm table-bordered mt-3">
    <!--
    <thead class="thead-dark">
        <th>Date</th>
        <th>Account</th>
        <th>Action</th>
        <th>Value</th>
        <th>Quantity</th>
        <th>Memo</th>
    </thead>
    -->
    <tbody>
        <tr class="table-secondary">
            <td>split.transaction.post_date</td>
            <td>split.transaction.description</td>
            <td colspan="2">split.transaction.notes</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>sp.account.fullname</td>
            <td>sp.action</td>
            <td>sp.memo</td>
            <td class="text-right">sp.value</td>
            <td class="text-right">sp.quantity</td>
        </tr>
    </tbody>
</table>
</div>
</template>
<script>
import vSelect from "vue-select"
import DatePicker from "vue2-datepicker"
import axios from "axios"

export default {
  data() {
    return {
      label: "label?",
      dateFrom: "",
      dateTo: "",
      account: "",
      options: []
    };
  },

  methods: {
    getOptions: function(search, loading) {
        if (search.length < 2) return;

        loading(true)

      axios.get("/account/api/search", {
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
  },

  components: {
    vSelect,
    DatePicker
  }
};
</script>
<style>

</style>
