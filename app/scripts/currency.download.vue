<docs>
Currency download page, implemented in vue.js.
</docs>

// import currency table

<template>
    <div>
        <h3>Book currencies</h3>
        <CurrencyTable currencies={this.state.currencies} />
        <div className="text-center">
            <button className="btn btn-primary" onClick={event => this.downloadAll(event)}>
                Download all
            </button>
            {this.state.importEnabled ?
                <button className="btn btn-outline-primary ml-3" onClick={event => this.importAll(event)}>
                    Import all
            </button>
                : null}
        </div>
    </div>
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
