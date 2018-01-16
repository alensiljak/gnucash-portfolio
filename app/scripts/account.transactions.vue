/**
    Account transactions
    - Incomplete! -
 */
<template>
<div>
<div class="card bg-secondary text-dark">
    <div class="card-header"></div>
    <div class="card-body">
        <form class="form">
            <div class="row">
                <!-- Account -->
                <div class="form-group col-md-7">
                    <!-- <label for="account">Account</label> -->
                    <v-select
                        class="form-control"
                        v-focus
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
                    <date-picker lang="en" name="dateFrom" placeholder="Date from" v-model="dateFrom"
                        :width="120" /> - 
                    <date-picker lang="en" name="dateTo" placeholder="Date to" v-model="dateTo"
                        :width="120" />
                </div>
            </div>
            <div class="form-row">
                <div class="text-center col-md">
                    <button type="button" class="btn btn-primary">Apply</button>
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

<b-table striped hover small :items="items"></b-table>


</div>
</template>
<script>
import vSelect from "vue-select";
import DatePicker from "vue2-datepicker";
import axios from "axios";
import BootstrapVue from "bootstrap-vue";
// import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

/**
    Focus directive.
    Used to focus on the account name search box.
 */
const focus = {
  inserted(el) {
    el.querySelector("input").focus();
  }
};

export default {
  directives: { focus },

  data() {
    return {
      dateFrom: "",
      dateTo: "",
      account: "",
      options: [],
      columns: ["name", "date", "value"],
      items: [{ name: "blah", date: "2018-01-10", value: "yo!" }]
    };
  },

  methods: {
    getOptions: function(search, loading) {
      if (search.length < 2) return;

      loading(true);

      axios
        .get("/account/api/search", {
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
    }
  },

  mounted: function() {
    // focus
    // set dates
    var from = new Date();
    from.setMonth(from.getMonth() - 3);
    this.dateFrom = from;

    var to = new Date();
    this.dateTo = to;
  },

  components: {
    vSelect,
    DatePicker,
    BootstrapVue
  }
};
</script>
<style>

</style>
