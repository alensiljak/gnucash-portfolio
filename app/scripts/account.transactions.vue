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
                        v-model="account"
                        class="form-control"
                        v-focus
                        :debounce="250"
                        :on-search="getAccounts"
                        :options="options"
                        placeholder="Search account..."
                        label="name"
                        :on-change="accountSelected"
                    ></v-select>
                </div>

                <!-- Date Period -->
                <div class="form-group col-md form-inline">
                    <input type="date" name="dateFrom" class="form-control" v-model="dateFrom"
                      @change="loadTransactions" /> -
                    <input type="date" name="dateTo" class="form-control" v-model="dateTo"
                      @change="loadTransactions" />

                    <b-alert variant="warning" :show="datesNotSelected">Dates not selected!</b-alert>

                    <span>
                      <a href="#" @click="setPeriod('7')">
                        <small>7 days</small>
                      </a>
                      &bullet;
                      <a href="#" @click="setPeriod('30')">
                        <small>30 days</small>
                      </a>
                      &bullet;
                      <a href="#" @click="setPeriod('90')">
                        <small>90 days</small>
                      </a>
                    </span>
                </div>

                <!-- apply button -->
                <div class="text-center col-md-1">
                    <button @click="loadTransactions" type="button" class="btn btn-primary">Apply</button>
                </div>

            </div>
        </form>
    </div>
</div>

<p>
    Transactions for account <strong>{{ model.accountName }}</strong> <br>
    Starting balance: <span>{{ model.startBalance }}</span>, Ending balance: {{ model.endBalance }}
</p>

<b-table striped hover small :fields="tableFields" :items="model.transactions">
  <template slot="date" slot-scope="data">
    <a :href="'/transaction/details/' + data.item.id">
    <!-- {{ data }} -->
    {{ data.value }}
    </a>
  </template>
  <template slot="value" slot-scope="data">
    {{ formatNumber(data.value) }}
  </template>
  <template slot="quantity" slot-scope="data">
    {{ formatNumber(data.value) }}
  </template>
</b-table>

</div>
</template>
<script>
import vSelect from "vue-select";
import axios from "axios";
import BootstrapVue from "bootstrap-vue";
// import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap-vue/dist/bootstrap-vue.css";
import format from 'number-format.js'

/**
    Focus directive.
    Used to focus on the account name search box.
 */
const focus = {
  inserted(el) {
    // don't focus if we have some data passed from the page.
    if (window.model) return

    el.querySelector("input").focus();
  }
};

Date.prototype.addDays = function(days) {
  var dat = new Date(this.valueOf());
  dat.setDate(dat.getDate() + days);
  return dat;
}

export default {
  directives: { focus },

  data() {
    return {
      dateFrom: "",
      dateTo: "",
      // Account selector
      account: "",
      options: [],
      // Validation
      datesNotSelected: false,
      // Table.
      tableFields: [
        "date",
        "description",
        "notes",
        {
          key: "value",
          tdClass: "text-right"
        },
        {
          key: "quantity",
          tdClass: "text-right"
        }
      ],
      model: {
        accountName: "",
        startBalance: 0,
        endBalance: 0,
        transactions: []
      }
    };
  },

  methods: {
    formatNumber: function(number) {
      return format("#,##0.00", number)
    },
    /**
        Load account list for dropdown.
       */
    getAccounts: function(search, loading) {
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
    },
    accountSelected: function(account) {
      if (!account) return;

      this.account = account;

      // re-load transactions
      this.loadTransactions();
    },
    loadTransactions: function() {
      // validations
      // TODO: check for all input fields: account, date range.
      this.datesNotSelected = !this.dateFrom || !this.dateTo;

      axios
        .get("/account/api/transactions", {
          params: {
            dateFrom: this.dateFrom,
            dateTo: this.dateTo,
            account: this.account.id
          }
        })
        .then(response => {
          this.model = response.data;
          // this.txRows = response.data.transactions
          // this.startBalance = response.startBalance
          // this.endBalance = response.endBalance
          if (!this.account.name) {
            this.account.name = this.model.accountName
          }
        })
        .catch(error => {
          console.error(error);
        });
    },
    isoDate(date) {
      // return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
      var result = date.toISOString().substring(0, 10);
      // console.log(result)
      return result;
    },
    setPeriod: function(days) {
      var from = new Date();
      //from.setMonth(from.getMonth() - 3);
      from = from.addDays(-days)
      this.dateFrom = this.isoDate(from)

      //today
      var to = new Date();
      this.dateTo = this.isoDate(to)

      this.loadTransactions()
    }
  },

  mounted: function() {
    // Focus is done with the custom directive. See above.

    // get the account id from the page
    if (window.model) {
      this.account = {
        id: window.model.accountId,
        name: ""
      };
    }

    // Initialize dates.
    this.setPeriod(7);
  },

  components: {
    vSelect,
    // DatePicker,
    BootstrapVue
  }
};
</script>
<style>

</style>
