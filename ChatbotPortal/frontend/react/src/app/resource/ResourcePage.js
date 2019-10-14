import React from 'react';
import axios from 'axios';
import {Container, Form, Rating, Button, Dropdown, Popup, Input} from 'semantic-ui-react';

export default class ResourcePage extends React.Component {
	constructor(props) {
		super(props);

		//TODO: Add search options here for tags...
		this.state = {
			tagOptions : [
				{ key: 'child', text: 'Child', value: 'child' },
				{ key: 'teenager', text: 'Teenager', value: 'teenager' },
				{ key: 'adult', text: 'adult', value: 'adult' },
			]
		};

		axios.get('/chatbotportal/resources/fetch-tags', {
			params : {
				name: 'young'
			}
		}).then(response => {
			console.log('I got here!');
			console.log(response);
		});
	}

	render() {
		return (
			<Container>
				<Form>
					<Form.Group>
						<Form.Field>
							<label>Enter URL</label>
							<Input placeholder="xxx@yyy.ca"/>
						</Form.Field>
						<Form.Field>
							<label>Rating</label>
							<Rating maxRating={5} defaultRating={3} icon='star' size='massive' />
						</Form.Field>
					</Form.Group>
					<Form.Group>
						<Form.Field>
							<label>Tags</label>
							<Form.Group>
								<Dropdown placeholder='Enter tags separated by commas' fluid multiple selection options={this.state.tagOptions} />
								<Popup trigger={<Button icon='add' />} flowing hoverable>
									<Input placeholder="New Tag"/>
									<Button>Submit</Button>
								</Popup>
							</Form.Group>
						</Form.Field>
						<Form.Field>
							<label>Comments</label>
							<Input placeholder="Enter any comments (Optional)"/>
						</Form.Field>
					</Form.Group>
					<Button type='submit'>Submit</Button>
				</Form>
			</Container>
		);
	}
}