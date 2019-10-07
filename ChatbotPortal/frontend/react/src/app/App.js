import React from 'react';

export default class App extends React.Component {
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
			<div>
				<p>Hello World!</p>
				<p>Counter:{this.state.counter}</p>
				<button onClick={this.onButtonClick}>Click me!</button>
			</div>
		);
	}
}