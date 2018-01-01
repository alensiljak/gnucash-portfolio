"use strict"
// template: https://github.com/vuejs-templates/webpack/blob/develop/template/config/index.js

const path = require('path')
const webpack = require('webpack')
var webpack = require('webpack')
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        site: "./scripts/site.js",
        currency_download: "./scripts/currency.download.js"
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
                test: /\.scss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    'sass-loader'
                ],
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
        // loaders: [
        //     {
        //         test: /\.vue$/,
        //         loader: 'vue'
        //     }
        // ]
    },

    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },

    plugins: [
        // Separate into vendor file all used libraries from node_modules.
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.[chunkhash].js',
            minChunks(module) {
                return module.context &&
                    module.context.indexOf('node_modules') >= 0;
            }
        }),
        // Copy all image files to /static folder.
        new CopyWebpackPlugin([
            // output is already pointing to /static.
            { from: 'images', to: './' }
        ]),

        // Provides "jquery" package whenever $ or jQuery is encountered.
        // new webpack.ProvidePlugin({
        //     $: "jquery",
        //     jQuery: "jquery"
        // })
    ],

    performance: {
        hints: false
    },

    devtool: '#eval-source-map'
    // devtool: 'source-map'
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
