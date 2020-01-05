const HtmlWebPackPlugin = require( 'html-webpack-plugin' );
const path = require('path');

module.exports = {
  entry: './app/app.js',            // Main entrypoint of the application
  context: __dirname,
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'index_bundle.js',    // Filename of the generated JS bundle that contains all application JS code
    publicPath: '/'                 // Base path for all assets within the application
  },
  devServer: {
    // redirect all server requests to /index.html which will download all the JS resources and
    // allow React Router to take it from there
    historyApiFallback: true
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(jpg|png)/,
        use: { loader: 'url-loader'}
      },
      {
        test: /\.s?css$/,
        oneOf: [
            {
              test: /\.module\.s?css$/,
              use: [
                "style-loader",
                {
                  loader: "css-loader",
                  options: { modules: true }
                },
                "sass-loader"
              ]
            },
            {
              test: /\.s?css$/,
              use: ["style-loader", "css-loader", "sass-loader"],
              exclude: /\.module\.s?css$/
            }
        ]
      },
    ]
  },
  plugins: [
      new HtmlWebPackPlugin({
         template: path.resolve( __dirname, 'public/index.html' ),
         filename: 'index.html'
      })
   ]
};