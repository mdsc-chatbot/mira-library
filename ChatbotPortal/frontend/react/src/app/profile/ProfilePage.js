import React, {Component} from 'react';
import {SecurityContext} from '../security/SecurityContext';
import EditForm from "./EditForm";


class ProfilePage extends Component {

	state = {
		token: '',
		displayed_form: 'edit',
		logged_in: localStorage.getItem('token') ? true : false,
		id: '',
		email: '',
		first_name: '',
		last_name: '',
		is_edited: false,
		url: ''
	};

	handle_edit = (e, data, setSecurity) => {
		e.preventDefault();
		fetch(`http://localhost:8000/4/update/`, {
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

// export default function ProfilePage() {
// 	return (
// 		<EditForm />
		// {/*<div>*/}
		// {/*	<SecurityContext.Consumer>*/}
        // {/*        {(securityContext) => (*/}
        // {/*        	<div>*/}
        // {/*                <h3>*/}
        // {/*                    {securityContext.security.logged_in*/}
        // {/*                        ? 	`Email: ${securityContext.security.email} '\n'*/}
        // {/*                        	 First Name: ${securityContext.security.first_name} '\n'*/}
        // {/*                        	 Last Name: ${securityContext.security.last_name} '\n'*/}
        // {/*                        	 Affiliation: ${securityContext.security.affiliation} '\n'*/}
        // {/*                        	 Active: ${securityContext.security.active} '\n'*/}
        // {/*                        	 Staff: ${securityContext.security.staff} '\n'*/}
        // {/*                        	 Admin: ${securityContext.security.admin}`*/}
        // {/*                        : 'No Security Context'}*/}
        // {/*                </h3>*/}
        // {/*            </div>*/}
        // {/*        )}*/}
        // {/*    </SecurityContext.Consumer>*/}
		// {/*</div>*/}
// 	);
// }