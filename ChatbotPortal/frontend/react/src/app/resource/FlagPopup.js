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
import {Button, Form, Checkbox, Popup, Icon} from 'semantic-ui-react';
import { SecurityContext } from "../contexts/SecurityContext";

export default class FlagPopup extends React.Component {
	static contextType = SecurityContext;

	constructor(props) {
		super(props);

		this.state = {
			flag_id : 1,
			isOpen : false,
		};
	}

	handleChange = (event, {value}) => {
		this.setState({
			flag_id : value
		});
	};

	handleSubmit = (event, data) => {
		event.preventDefault();

		axios.post(`/chatbotportal/resource/flag-resource/`,
		{
			resource_id : this.props.resource_id,
			flag_id : this.state.flag_id
		},{
			headers: {Authorization: `Bearer ${this.context.security.token}`}
		});

		this.setState({ isOpen: false })
	};

	render() {
		return (
			<Popup trigger={<Icon name='exclamation circle' color='red' />} on='click' open={this.state.isOpen} onOpen={()=>this.setState({ isOpen: true })} onClose={()=>this.setState({ isOpen: false })} flowing>
				<Form>
					<h4>Report an Issue with this resource</h4>
					<Form.Field>
						<Checkbox
						radio
						label='Some information is incorrect'
						name='checkboxRadioGroup'
						value={1}
						checked={this.state.flag_id === 1}
						onChange={this.handleChange}
						/>
					</Form.Field>
					<Form.Field>
						<Checkbox
						radio
						label='Resource is unavailable'
						name='checkboxRadioGroup'
						value={2}
						checked={this.state.flag_id === 2}
						onChange={this.handleChange}
						/>
					</Form.Field>
					<Form.Field>
						<Checkbox
						radio
						label='This resource should not have been approved'
						name='checkboxRadioGroup'
						value={3}
						checked={this.state.flag_id === 3}
						onChange={this.handleChange}
						/>
					</Form.Field>
					<Form.Field>
						<Checkbox
						radio
						label='Other Issue'
						name='checkboxRadioGroup'
						value={4}
						checked={this.state.flag_id === 4}
						onChange={this.handleChange}
						/>
					</Form.Field>
					<Button onClick={this.handleSubmit}>Submit</Button>
				</Form>
			</Popup>
		);
	}
}

FlagPopup.propTypes = {
	resource_id : PropTypes.number,
};