<docs>
Currency table row component.
</docs>

<template>
    <tr key={this.state.currency.symbol}>
        <td>
            {this.state.currency.symbol}
        </td>
        <td>{this.state.currency.rate}</td>
        <td>
            {this.state.currency.rateDate}
        </td>
        <td>
            {indicator}
        </td>
    </tr>
</template>
<script>
export default {
  data() {
    return {
      msg: "Hello world!"
    };
  }
};
</script>
