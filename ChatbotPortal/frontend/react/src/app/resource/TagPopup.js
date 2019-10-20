import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import {Button, Form, Input, Popup, Label} from 'semantic-ui-react';

export default class TagPopup extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			value : '',
			validation : null,
		};
	}

	handleChange = (event, {value}) => {
		this.setState({
			validation : null,
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
		})
			.then(response => {
				this.props.onNewTag(response.data);
				this.setState({
					value : ''
				});
			})
			.catch(error => {
				this.setState({
					validation : error.response.data.name
				});
		});
	};

	render() {
		return (
			<Popup trigger={<Button icon='add' onClick={event => event.preventDefault()} />} flowing hoverable>
				<Form>
					{this.state.validation ? (
						<Label basic color='red' pointing='below'>{this.state.validation}</Label>
					) : null}
					<Form.Group>
						<Input
							error={!!this.state.validation}
							placeholder="New Tag"
							onChange={this.handleChange}
							value={this.state.value}
						/>
						<Button onClick={this.handleSubmit}>Submit</Button>
					</Form.Group>
				</Form>
			</Popup>
		);
	}
}

TagPopup.propTypes = {
	onNewTag : PropTypes.func,
};