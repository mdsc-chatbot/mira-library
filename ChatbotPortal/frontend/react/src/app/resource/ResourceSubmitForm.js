import React, { Component } from 'react'
import {Container, Form, Rating, Button} from 'semantic-ui-react';

export default class ResourceSubmitForm extends Component {
    render() {
        return (
            <Container>
				<Form>
					<Form.Group>
						<Form.Field>
							<label>Enter URL</label>
							<input placeholder="xxx@yyy.ca"/>
						</Form.Field>
						<Form.Field>
							<label>Rating</label>
							<Rating maxRating={5} defaultRating={3} icon='star' size='massive' />
						</Form.Field>
					</Form.Group>
					<Form.Group>
						<Form.Field>
							<label>Tags</label>
							<input placeholder="Enter tags separated by commas"/>
						</Form.Field>
						<Form.Field>
							<label>Comments</label>
							<input placeholder="Enter any comments (Optional)"/>
						</Form.Field>
					</Form.Group>
					<Button type='submit'>Submit</Button>
				</Form>
			</Container>
        )
    }
}

