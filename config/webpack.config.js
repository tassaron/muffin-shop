const webpack = require("webpack");

module.exports = (env, argv) => {
    const config = {
        entry: __dirname + "/../src/react/main.jsx",
        output: {
            path: __dirname + "/../static/js/dist",
            filename: "bundle.js",
        },
        resolve: {
            extensions: [".js", ".jsx", ".css"],
        },
    
        module: {
            rules: [
                {
                    test: /\.(js|jsx)?/,
                    exclude: /node_modules/,
                    loader: "babel-loader",
                    options: {
                        presets: [
                            "@babel/preset-env",
                            ["@babel/preset-react", { runtime: "automatic" }],
                        ],
                    },
                },
                {
                    test: /\.css?/,
                    exclude: /node_modules/,
                    use: ["style-loader", "css-loader"],
                },
            ],
        },
    };
    if (argv.mode == "production") {
        const TerserPlugin = require('terser-webpack-plugin');
        config.optimization = {
            minimizer: [new TerserPlugin({})],
        }
    }
    return config
};
