/**
 * @file: PasswordResetPage.js
 * @summary: Renders the password reset form from the email confirmation link
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

import React from 'react';
import {Button, Form, Grid, Header, Segment} from 'semantic-ui-react';
import axios from 'axios';
import {baseRoute} from '../App';
import { SecurityContext } from "../contexts/SecurityContext";

/**
 * This class performs the password change operation after a password change request.
 */
class PasswordResetPage extends React.Component {
    static contextType = SecurityContext;

    /**
     * This construct initializes the state.
     * @param props
     */
    constructor(props) {
        super(props);
        /**
         * The state of the component
         * @type {{uid: number, new_password1: string, new_password2: string, password_matched: boolean, token: *}}
         */
        this.state = {
            uid: this.props.match.params.uid,
            token: this.props.match.params.token,
            new_password1: "",
            new_password2: "",
            password_matched: false,
            reset_error: false
        };
    }

    /**
     * This function changes the password by calling the backend API
     * @param e = event
     * @param passwordFormData = Data procured from the password form
     */
    handle_password = (e, passwordFormData) => {
        /**
         * If the password fields matches, then call the backend API to reset password
         */
        if (this.state.password_matched) {
            const url = `/chatbotportal/authentication/password/reset/confirm/${this.state.uid}/${this.state.token}/`;

            axios
                .post(url, passwordFormData)
                .then(
                    response => {
                        console.log(response);
                        this.setState({ reset_error: false });
                        // Upon successful changing of password, redirect the user to the login page
                        window.location = `${baseRoute}/login`;
                    },
                    error => {
                        console.log(error);
                        this.setState({ reset_error: true });
                    }
                );
        }
    };

    /**
     * This function handles the changes that happens to the first password field.
     * @param e = event
     */
    handle_password1 = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevstate => {
            const newState = { ...prevstate };
            newState[name] = value;
            return newState;
        });
    };

    /**
     * This function handles the changes that happens to the second password field.
     * @param e = event
     */
    handle_password2 = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevstate => {
            const newState = { ...prevstate };
            newState[name] = value;
            return newState;
        });

        /**
         * Matching both the field to enable reset call
         */
        if (value !== null && value === this.state.new_password1) {
            this.setState({
                password_matched: true
            });
        } else {
            this.setState({
                password_matched: false
            });
        }
    };

    render() {
        return (
            <Grid
                // onSubmit={e => this.handle_password(e, this.state)}
                textAlign="center"
                style={{ height: "100vh" }}
                verticalAlign="middle"
            >
                <Grid.Column style={{ maxWidth: 450 }}>
                    <Header as="h2" color="blue" textAlign="center">
                        {/*<Image src='/logo.png'/> */}
                        Password Reset
                    </Header>

                    <Form size="large">
                        <Segment stacked>
                            <Form.Input
                                fluid
                                icon="lock"
                                iconPosition="left"
                                placeholder="Password (must be at least 8 characters)"
                                type="password"
                                name="new_password1"
                                value={this.state.new_password1}
                                onChange={this.handle_password1}
                            />
                            <Form.Input
                                fluid
                                icon="lock"
                                iconPosition="left"
                                placeholder="Confirm Password"
                                type="password"
                                name="new_password2"
                                value={this.state.new_password2}
                                onChange={this.handle_password2}
                            />

                            {this.state.reset_error === true ? (
                                <Button
                                    color="red"
                                    fluid
                                    size="medium"
                                    name="password_reset_request_page_button"
                                    content="Unable to reset! Please request password reset email again."
                                    onClick={() => {
                                        window.location = `${baseRoute}/password/reset`;
                                    }}
                                />
                            ) : (
                                <Button
                                    color="blue"
                                    fluid
                                    size="medium"
                                    name="password_reset_button"
                                    content="Submit"
                                    disabled={
                                        !(this.state.new_password1.length >= 8) ||
                                        !this.state.password_matched
                                    }
                                    onClick={e => this.handle_password(e, this.state)}
                                />
                            )}
                        </Segment>
                    </Form>
                </Grid.Column>
            </Grid>
        );
    }
}

export default PasswordResetPage;