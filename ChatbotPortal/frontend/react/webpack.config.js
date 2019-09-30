// Build Configuration
// Feel free to change this boolean freely until we figure out how to switch between DEV and PROD mode
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const productionMode = true;
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
		// this plugin builds our HTML file using the provided template
		new HtmlWebpackPlugin({
			template : 'src/index.html',
			meta : {
				'timesheet.dateFormat' : 'YYYY-MMM-DD', // also set in JsonConfig.java
			}
		}),
	],
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
				test: /\.(css|scss)$/,
				include : [/node_modules/],
				use: [
					{ loader: 'style-loader' },
					{ loader: 'css-loader' },
					{ loader: 'sass-loader' }
				]
			},
		]
	}
}