/**
 * @file: LoginPage.js
 * @summary: Declares the function require for login related functions, and renders login form.
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

import React, {Component} from 'react';
import axios from "axios";
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import {SecurityContext} from '../contexts/SecurityContext';
import {Redirect} from "react-router";
import {baseRoute} from "../App";
import {Message} from "semantic-ui-react";


class LoginPage extends Component {
    /**
     * The LoginPage that will render the login form
     * and communicate with the backend.
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    constructor(props) {
        /**
         * A constructor that defines state with properties
         */
        super(props);

        /** State displayed_form determines which form to display
         * @type {{
         *      signup_error: boolean,
         *      login_error: boolean,
         *      displayed_form: string,
         *      message: string,
         *      signup_success: boolean}}
         */
        this.state = {
            displayed_form: 'login',
            message: '',
            signup_success: false,
            signup_error: false,
            login_error: false
        };
    }

    componentDidMount() {
        /**
         * When component get mounted check if the user is already logged in.
         */
        if (this.context.security.logged_in) {
            axios.get(
                '/chatbotportal/authentication/retrieve',
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
            .post('/chatbotportal/authentication/login/', loginFormData)
            .then(
                response => {
                    if (response.status === 200) {
                        response.data['is_logged_in'] = true;
                        this.context.setSecurity(response.data);
                        this.setState({login_error: false});
                        localStorage.setItem('token',response.data.token)
                        console.log(this.context.security);
                    } else if (response.status === 203) {
                        this.setState({message: response.data.message, login_error: true});
                    }
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
            .post('/chatbotportal/authentication/register/', signupFormData)
            .then(
                response => {
                    if (response.status === 201) {
                        this.setState({
                            message: response.data.message,
                            signup_success: true,
                            signup_error: false
                        });
                    } else if (response.status === 226) {
                        this.setState({
                            message: response.data.message,
                            signup_success: false,
                            signup_error: true
                        });
                    }
                },
                error => {
                    console.log(error + ": User did not get created.")
                }
            );
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
                            this.state.signup_error === true && this.state.signup_success === false ? (
                                <Message
                                    error
                                    header='Already exists!'
                                    content={this.state.message}
                                />
                            ) : null
                        }
                        {
                            this.state.login_error === true ? (
                                <Message
                                    error
                                    header='Unsuccessful Login!'
                                    content={this.state.message}
                                />
                            ) : null
                        }

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

                        {
                            this.state.signup_error === false && this.state.signup_success === true ? (
                                <Redirect
                                    to={{
                                        pathname: baseRoute + '/validate/email',
                                        state: {message: this.state.message}
                                    }}
                                />
                            ) : null
                        }

                        {
                            securityContext.security.is_logged_in ? (
                                <Redirect to={baseRoute}/>
                            ) : null
                        }
                    </div>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default LoginPage;