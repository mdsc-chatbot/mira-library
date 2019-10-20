// Build Configuration
// Feel free to change this boolean freely until we figure out how to switch between DEV and PROD mode
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const productionMode = false;
const environment = productionMode ? 'production' : 'development';
const sourceMaps = productionMode;

module.exports = {
	mode : environment,
	devtool : sourceMaps ? 'false' : 'eval-source-map',
	entry: {
		app : ['./src/index.js']
	},
	output : {
		filename : 'js/[name]-[chunkhash].js',
		path : path.resolve(__dirname, './webpack'),
		publicPath: '/chatbotportal/resources/'
	},
	plugins : [
		// this plugins cleans our build directory of old HTML/JS files
		new CleanWebpackPlugin(),
		// this plugin builds our HTML file using the provided template
		new HtmlWebpackPlugin({
			template : 'src/index.html',
			// meta : {
			// 	'timesheet.dateFormat' : 'YYYY-MMM-DD',
			// }
		}),
		new MiniCssExtractPlugin({
			// Options similar to the same options in webpackOptions.output
			// both options are optional
			filename: "[name].css",
			chunkFilename: "[id].css"
		})
	],
	resolve: {
		alias: {
			"../../theme.config$": path.join(__dirname, "/semantic-ui/theme.config"),
			"../semantic-ui/site": path.join(__dirname, "/semantic-ui/site")
		}
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: {
					loader: "babel-loader"
				}
			},
			{
				test: /\.(css)$/,
				use: [
					{
						loader: MiniCssExtractPlugin.loader,
						options: {
							// you can specify a publicPath here
							// by default it uses publicPath in webpackOptions.output
							// publicPath: '../',
							hmr: process.env.NODE_ENV === 'development',
						},
					},
					{
						loader: 'css-loader',
						options: {
							sourceMap: true,
							modules: {
								localIdentName: '[name]__[local]____[hash:base64:5]',
							},
						},
					},
				]
			},
			{
				test:  /\.(less)$/,
				include : [/node_modules/],
				use: [
					MiniCssExtractPlugin.loader,
					"css-loader",
					"less-loader"
				]
			},
			{
				test: /\.woff($|\?)|\.woff2($|\?)|\.ttf($|\?)|\.eot($|\?)|\.svg($|\?)/,
				use: "url-loader"
			},
			{
				test: /\.(png|jpe?g|gif)$/i,
				use: [
					{
						loader: 'file-loader',
					},
				],
			},
		]
	}
}