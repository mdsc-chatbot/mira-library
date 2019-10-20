import React, {Component} from 'react';
import {SecurityContext} from '../security/SecurityContext';
import EditForm from "./EditForm";


class ProfilePage extends Component {

	static contextType = SecurityContext;

	constructor(props){
		super(props);
		this.state = {
			token: '',
			displayed_form: 'edit',
			logged_in: '',
			id: '',
			email: '',
			first_name: '',
			last_name: '',
			is_edited: false,
			url: ''
		};
	}

	componentDidMount() {
        if (this.context.security.logged_in) {

            this.setState({
                logged_in: this.context.security.logged_in,
				token: this.context.security.token,
                id: this.context.security.id,
                email: this.context.security.email,
                first_name: this.context.security.first_name,
                last_name: this.context.security.last_name,
                is_edited: false,
            })
        }
    }

	handle_edit = (e, data, setSecurity) => {
		e.preventDefault();
		fetch(`http://localhost:8000/signup/${this.state.id}/update/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json'
			},
			body: JSON.stringify(data)
		})
			.then(res => res.json())
			.then(json => {
				setSecurity({
					logged_in: true,
					id: json.id,
					email: json.email,
					first_name: json.first_name,
					last_name: json.last_name
				});
				this.setState({
                    logged_in: true,
                    id: json.id,
                    email: json.email,
                    first_name: json.first_name,
                    last_name: json.last_name,
                });
			});
	};

	updateURL = pk => {
		this.setState({
			url: `http://localhost:8000/${pk}/update/`
		})
	};

	is_edited = () => {
		this.setState({
			edited: true
		});
	};

	render() {
		return(
			<SecurityContext.Consumer>
				{(securityContext) => (
					<div className="App">
						<EditForm
							handle_edit={(event, data) => this.handle_edit(event, data, securityContext.setSecurity)}
						 	is_edited={this.is_edited}
						/>

						<h3>
                            {securityContext.security.edited
                                ? `Edited${securityContext.security.first_name}`
                                : 'Please Edit'}
                        </h3>
					</div>
				)}
			</SecurityContext.Consumer>
		);
	}
}

export default ProfilePage;
