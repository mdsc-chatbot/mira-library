/**
 * @file: Logout.js
 * @summary: Component that handles logout related functions
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
import {SecurityContext} from '../contexts/SecurityContext';
import {Redirect} from "react-router";
import {baseRoute} from "../App";


class LogoutPage extends Component {
    /**
     * The LoginPage that will render the login form
     * and communicate with the backend.
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

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
            .get('/chatbotportal/authentication/logout/', {headers: options})
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
            <Redirect to={baseRoute}/>
        );
    }
}

export default LogoutPage;