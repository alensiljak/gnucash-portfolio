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
            <input type="hidden" name="account_id" value="{{ input_model.account_id }}">
            <div class="form-group">
                <label for="account">Account</label>
                <div class="text-dark">
                        <type-ahead />
                </div>
            </div>

            <!-- Date Period -->
            <div class="form-group">
                <label for="period">Period</label>
                <input id="period" type="text" name="period" class="form-control daterange" {% if input_model.period %}value="{{ input_model.period }}"
                    {% endif %}>
            </div>

            <div class="text-center">
                <button id="submit" class="btn btn-primary">Apply</button>
            </div>
        </form>
    </div>
</div>

<p>
    Starting balance: {{ "{:,.2f}".format(model.start_balance) }}, Ending balance: {{ "{:,.2f}".format(model.end_balance) }}
</p>

{% if model.splits %}
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
        {% for split in model.splits %}
        <tr class="table-secondary">
            <td>{{ "{:%Y-%m-%d}".format(split.transaction.post_date) }}</td>
            <td>{{ split.transaction.description }}</td>
            <td colspan="2">{{ split.transaction.notes }}</td>
        </tr>
        {% for sp in split.transaction.splits %}
        <tr>
            <td>&nbsp;</td>
            <td>{{ sp.account.fullname }}</td>
            {#
            <td>{{ sp.action }}</td> #}
            <td>{{ sp.memo }}</td>
            {#
            <td class="text-right">{{ sp.value }}</td> #}
            <td class="text-right">{{ "{:,.2f}".format(sp.quantity) }}</td>
        </tr>
        {% endfor %} {% endfor %}
    </tbody>
</table>
</div>
</template>
<script>
import TypeAhead from 'vue2-typeahead';

export default {
    data() {

    },

    methods: {

    },

    components: {
        TypeAhead
    }
}
</script>
<style>
</style>