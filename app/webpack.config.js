"use strict"
// template: https://github.com/vuejs-templates/webpack/blob/develop/template/config/index.js

const path = require('path')
const webpack = require('webpack')
const CopyWebpackPlugin = require('copy-webpack-plugin');   // Copy files to destination.
const CleanWebpackPlugin = require('clean-webpack-plugin'); // Clean destination folder.
const ExtractTextPlugin = require('extract-text-webpack-plugin');
// const siteSCSS = new ExtractTextPlugin('styles/site.scss');

module.exports = {
    entry: {
        // Vendor .js
        vendor1: "./scripts/vendor.js",
        site: "./scripts/site.js",
        // Custom .js
        account_transactions: "./scripts/account.transactions.js",
        currency_download: "./scripts/currency.download.js",
        currency_calculator: "./scripts/currency.calculator.js",
        scheduled_calendar: "./scripts/scheduled.calendar.js",
        securities: "./scripts/securities.js",
        security_prices: "./scripts/security.prices.js",
        // Styles
        styles: "./styles/styles.scss",
    },

    output: {
        path: path.resolve(__dirname, 'static'),
        filename: '[name].js'
        // [chunkhash]
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ],
            },
            {
                test: /styles\.scss$/,
                loader: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [{
                        loader: 'css-loader',
                        options: {
                            minimize: true,
                            sourceMap: true
                        }
                    }, {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    }]
                })
            },
            {
                test: /\.scss$/,
                exclude: /styles\.scss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        // extract all <docs> content as raw text
                        //'docs': ExtractTextPlugin.extract('raw-loader'),
                    }
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            }
        ]
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },

    plugins: [
        new CleanWebpackPlugin(['static'], { verbose: true }),

        // Copy all image files to /static folder.
        new CopyWebpackPlugin([
            // output is already pointing to /static.
            { from: 'images', to: './' }
        ]),

        // Separate into vendor file all used libraries from node_modules.
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.webpack.js',
            // [chunkhash]
            minChunks(module) {
                return module.context &&
                    module.context.indexOf('node_modules') >= 0;
            }
        }),

        new ExtractTextPlugin("styles.css"),
        // new ExtractTextPlugin({ filename: 'bundle.css', disable: false, allChunks: true }),
        // siteSCSS

        // Provides "jquery" package whenever $ or jQuery is encountered.
        // new webpack.ProvidePlugin({
        //     $: "jquery",
        //     jQuery: "jquery"
        // })
    ],

    performance: {
        hints: false
    },

    // eval = inline source map
    // devtool: '#eval-source-map'
    // source map = separate .map file
    devtool: 'source-map'
}

// Development configuration

if (process.env.NODE_ENV === "development") {
    // Watch source folders for changes in dev mode.
    module.exports.watch = "true",

        module.exports.watchOptions = {
            ignored: /node_modules/
        },

        module.exports.plugins = (module.exports.plugins || []).concat([
            // minify only the vendor package
            new webpack.optimize.UglifyJsPlugin({
                test: /vendor\..*\.js$/,
                compress: { warnings: false },
                sourceMap: true
            })
        ])
}

// Production configuration

if (process.env.NODE_ENV === 'production') {
    // module.exports.devtool = '#source-map'
    module.exports.devtool = 'cheap-module-source-map';

    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: { warnings: false }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        })
    ])
}
