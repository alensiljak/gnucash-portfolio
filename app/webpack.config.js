const path = require('path');

module.exports = {
    entry: {
        site: "./scripts/site.js"
    },
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: '[name].js'
    }
}