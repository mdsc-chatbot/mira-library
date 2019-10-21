import React from 'react';
import {Container} from 'semantic-ui-react';

export default class HomePage extends React.Component {
	constructor(props){
		super(props);

		this.state = {
			counter : 0
		};
	}

	onButtonClick = (event) => {
		event.preventDefault();
		this.setState((prevState) => ({
			counter : prevState.counter + 1
		}));
	};

	render() {
		return (
			<Container>
				<h2>Welcome to ChatbotPortal!</h2>
				<p>This is an example page that will show the public feed in the future.</p>
			</Container>
		);
	}
}