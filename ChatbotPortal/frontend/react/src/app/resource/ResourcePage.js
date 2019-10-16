import React from 'react';
import {Container, Form, Rating, Button, Popup, Input} from 'semantic-ui-react';
import TagDropdown from './TagDropdown';
import TagPopup from './TagPopup';

export default class ResourcePage extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			currentTags : null
		};
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
								<TagDropdown onChange={currentTags => this.setState({currentTags})}/>
								<TagPopup />
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