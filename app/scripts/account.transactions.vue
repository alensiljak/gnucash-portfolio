/**
    Account transactions
    - Incomplete! -
 */
<template>
<div>
<div class="card bg-secondary text-dark">
    <div class="card-header"></div>
    <div class="card-body">
        <form action="/account/transactions" method="POST">
            <!-- Account -->
            <div class="form-group">
                <label for="account">Account</label>
                <div class="text-dark">
                    <type-ahead />
                </div>
            </div>

            <!-- Date Period -->
            <div class="form-group">
                <label for="period">Period</label>
                <date-picker lang="en" /> - <date-picker lang="en" />
            </div>

            <div class="text-center">
                <button id="submit" class="btn btn-primary">Apply</button>
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
import TypeAhead from 'vue2-typeahead';
import DatePicker from 'vue2-datepicker';

export default {
    data() {
        return {

        }
    },

    methods: {

    },

    components: {
        TypeAhead,
        DatePicker
    }
}
</script>
<style>
</style>