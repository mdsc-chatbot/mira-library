import React from 'react';
import ResourceList from './ResourceList'

export default class App extends React.Component {

	render() {
		return (
			<div>
				<h3> Resource List </h3>
				<ResourceList />
			</div>
		);
	}
}