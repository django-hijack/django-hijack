const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const path = require('path')

module.exports = {
  entry: {
    hijack: [
      './hijack/static/hijack/hijack.js',
      './hijack/static/hijack/hijack.scss'
    ]
  },
  output: {
    filename: '[name].min.js',
    path: path.resolve(process.env.BUILD_LIB || __dirname, 'hijack', 'static', 'hijack'),
    clean: false
  },
  plugins: [new MiniCssExtractPlugin({ filename: '[name].min.css' })],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }
    ]
  }
}
