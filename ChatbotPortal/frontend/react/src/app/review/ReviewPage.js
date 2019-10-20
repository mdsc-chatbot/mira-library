import React from 'react';
import ReviewTable from './ReviewTable';

export default class ResourcePage extends React.Component {
	constructor(props) {
	  super(props);
	}
  
	render() {
	  return (
		  <container>
			<ReviewTable />
		  </container>
	  );
	}
  }