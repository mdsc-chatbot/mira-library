import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import HomePage from "../Homepage";


class LogoutPage extends Component {
    /**
     * The LoginPage that will render the login form
     * and communicate with the backend.
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    BASE_AUTH_URL = 'http://127.0.0.1:8000/authentication/auth/';

    componentDidMount() {
        this.handle_logout();
    }

    /**
     * This function handles logout operation
     */
    handle_logout = () => {

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        /**
         * This function handles the logout by setting
         */
        axios
            .get(this.BASE_AUTH_URL + 'logout/', {headers: options})
            .then(
                response => {
                    if (response.data['user'] === 'AnonymousUser') {
                        this.context.setSecurity({
                            is_logged_in: false
                        });
                    }
                },
                error => {
                    console.log(error);
                }
            )
    };
    /**
     * This renders the LoginForm and SignupForm
     * @returns {SecurityContext.Consumer}
     */
    render() {
        return (
            <HomePage/>
        );
    }
}

export default LogoutPage;