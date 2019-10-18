import React from 'react';
import styles from './Homepage.css'

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
			<div>
				<p>Hello World! This text is <h1 className={styles.test}>yellow!</h1></p>
				<p>Counter:{this.state.counter}</p>
				<button onClick={this.onButtonClick}>Click me!</button>
			</div>
		);
	}
}