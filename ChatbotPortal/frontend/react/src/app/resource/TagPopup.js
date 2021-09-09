/**
 * @file: TagPopup.js
 * @summary: Semanitc UI Popup component allows user to input a new tag to be reviewed
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import {Button, Form, Input, Popup, Label} from 'semantic-ui-react';
import { SecurityContext } from "../contexts/SecurityContext";

export default class TagPopup extends React.Component {
	static contextType = SecurityContext;

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
		event.preventDefault();

		axios.post('/chatbotportal/resource/create-tag', {
			name : this.state.value
		},{
			headers: {Authorization: `Bearer ${this.context.security.token}`}
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
							spellcheck='true'
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