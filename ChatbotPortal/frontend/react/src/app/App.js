import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import BaseRouter from './routes';

import ResourceList from './ResourceList'

export default class App extends React.Component {

	render() {
		return (
			<div>
				<Router>
					<h3> Resources </h3>
					<BaseRouter />
				</Router>
			</div>
		);
	}
}