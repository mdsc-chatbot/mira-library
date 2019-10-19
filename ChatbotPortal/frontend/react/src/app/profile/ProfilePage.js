import React from 'react';
import Profile from "./Profile";
import {SecurityContext} from '../security/SecurityContext';
import Nav from "../authentication/Nav";
import LoginForm from "../authentication/LoginForm";

export default function ProfilePage() {
	return (
		<div>
			<h1>Making changes to profile page</h1>
			<Profile/>
			<SecurityContext.Consumer>
                {(securityContext) => (
                	<div>
                        <h3>
                            {securityContext.security.logged_in
                                ? 	`Email: ${securityContext.security.email} '\n'
                                	 First Name: ${securityContext.security.first_name} '\n'
                                	 Last Name: ${securityContext.security.last_name} '\n'
                                	 Affiliation: ${securityContext.security.affiliation} '\n'
                                	 Active: ${securityContext.security.active} '\n'
                                	 Staff: ${securityContext.security.staff} '\n'
                                	 Admin: ${securityContext.security.admin}`
                                : 'No Security Context'}
                        </h3>
                    </div>
                )}
            </SecurityContext.Consumer>
		</div>
	);
}