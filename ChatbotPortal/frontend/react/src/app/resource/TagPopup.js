import React from 'react';
import axios from 'axios';
import {Button, Input, Popup} from 'semantic-ui-react';

export default class TagPopup extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			value : ''
		};
	}

	handleChange = (event, {value}) => {
		this.setState({
			value
		});
	};

	handleSubmit = (event, data) => {
		//TODO: Use return value from post method somehow...
		event.preventDefault();
		axios.post('/chatbotportal/resource/create-tag', {
			name : this.state.value
		}, {
			headers: {"Content-Type": "application/json"},
		});
		this.setState({
			value : ''
		});
	};

	render() {
		return (
			<Popup trigger={<Button icon='add' onClick={event => event.preventDefault()} />} flowing hoverable>
				<Input placeholder="New Tag" onChange={this.handleChange} value={this.state.value}/>
				<Button onClick={this.handleSubmit}>Submit</Button>
			</Popup>
		);
	}
}