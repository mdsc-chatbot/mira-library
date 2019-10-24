import React, {Component} from 'react';
import axios from "axios";
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import {SecurityContext} from '../security/SecurityContext';


class LoginPage extends Component {
    /**
     * The LoginPage that will render the login form
     * and communicate with the backend.
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    BASE_AUTH_URL = 'http://127.0.0.1:8000/authentication/auth/';

    constructor(props) {
        /**
         * A constructor that defines state with properties
         */
        super(props);
        /**
         * State displayed_form determines which form to display
         * @type {
         *          {
         *              displayed_form: string}
         *          }
         */
        this.state = {
            displayed_form: 'login'
        };
    }

    componentDidMount() {
        /**
         * When component get mounted check if the user is already logged in.
         */
        if (this.context.security.logged_in) {
            axios.get(
                this.BASE_AUTH_URL + 'retrieve',
                {
                    headers: {'Authorization': `Bearer ${this.context.security.token}`}
                }
            ).then(response => {
                console.log(response.data);
                console.log(response.data.token);
            });
        }
    }

    /**
     * This function handles the overall login operations
     * @param e : event
     * @param loginFormData : data from LoginForm upon submission
     */
    handle_login = (e, loginFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();

        /**
         * Perform a post request for login.
         * Upon successful response, set the security context with response data.
         * Otherwise, send an error message saying "Forgot password?"
         */
        axios
            .post(this.BASE_AUTH_URL + 'login/', loginFormData)
            .then(
                response => {
                    response.data['is_logged_in'] = true;
                    this.context.setSecurity(response.data);
                    console.log(this.context.security)
                },
                error => {
                    console.log(error)
                }
            );
    };

    /**
     * This function handles the overall signup operations
     * @param e : event
     * @param signupFormData : data from SignupForm upon submission
     */
    handle_signup = (e, signupFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();

        /**
         * Perform a post request for signup.
         * Upon successful response, the user gets created.
         * Otherwise, send an error message saying "User was not created. Try again."
         */
        axios
            .post(this.BASE_AUTH_URL + 'register/', signupFormData)
            .then(
                response => {
                    console.log(response.status + ": User got created.")
                },
                error => {
                    console.log(error + ": User did not get created.")
                }
            );
    };

    /**
     * This function handles logout operation
     */
    handle_logout = () => {
        /**
         * This function handles the logout by setting
         */
        this.context.setSecurity({
            is_logged_in: false
        });
    };

    /**
     * This function sets the display_form state
     * to navigate to different forms.
     * @param form : String
     */
    display_form = form => {
        this.setState({
            displayed_form: form
        });
    };

    /**
     * This renders the LoginForm and SignupForm
     * @returns {SecurityContext.Consumer}
     */
    render() {
        return (
            <SecurityContext.Consumer>
                {(securityContext) => (
                    <div className="App">
                        {
                            this.state.displayed_form === 'login' ? (
                                <LoginForm
                                    handle_login={(event, data) => this.handle_login(event, data)}
                                    handleRegisterClicked={this.display_form}
                                />
                            ) : this.state.displayed_form === 'signup' ? (
                                <SignupForm
                                    handle_signup={(event, data) => this.handle_signup(event, data)}
                                    handleLoginClicked={this.display_form}
                                />
                            ) : null
                        }
                        <h3>
                            {securityContext.security.is_logged_in
                                ? `Hello, ${securityContext.security.id}`
                                : 'Please Log In'}
                        </h3>
                    </div>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default LoginPage;