const webpack = require('webpack');
const config = {
    entry:  __dirname + '/react/main.jsx',
    output: {
        path: __dirname + '/../../static/js/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    mode: "development",
 
    module: {
        rules: [
            {
                test: /\.(js|jsx)?/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: [
                        "@babel/preset-env",
                        ["@babel/preset-react", {"runtime": "automatic"}]
                    ],
                  },
            },
            {
                test: /\.css?/,
                exclude: /node_modules/,
                use: ['style-loader', 'css-loader']
            }        
        ]
    }
};
module.exports = config;