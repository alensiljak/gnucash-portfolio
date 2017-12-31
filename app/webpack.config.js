"use strict"
// template: https://github.com/vuejs-templates/webpack/blob/develop/template/config/index.js

const path = require('path')
var webpack = require('webpack')

module.exports = {
    entry: {
        site: "./scripts/site.js",
        currency_download: "./scripts/currency.download.js"
    },

    output: {
        path: path.resolve(__dirname, 'static'),
        filename: '[name].js'
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

    devtool: '#eval-source-map'
}

// Development configuration

if (process.env.NODE_ENV === "development") {
    module.exports.watch = "true",
        module.exports.watchOptions = {
            ignored: /node_modules/
        }
}

// Production configuration

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map'
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        })
    ])
}
