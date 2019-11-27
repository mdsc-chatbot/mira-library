/**
 * @file: LoginForm.js
 * @summary: The user interactive form component
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

import React from "react";
import PropTypes from "prop-types";
import {Button, Form, Grid, Header, Message, Segment} from "semantic-ui-react";
import {baseRoute} from "../App";

class LoginForm extends React.Component {
    /**
     * This class manages the Login form
     * @type {
     *      {
     *          password: string,
     *          email: string}
     *      }
     */
    state = {
        email: "",
        password: ""
    };

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevstate => {
            const newState = {...prevstate};
            newState[name] = value;
            return newState;
        });
    };

    render() {
        return (
            <Grid
                onSubmit={e => this.props.handle_login(e, this.state)}
                textAlign="center"
                style={{height: "100vh"}}
                verticalAlign="middle"
            >
                <Grid.Column style={{maxWidth: 450}}>
                    <Header as="h2" color="blue" textAlign="center">
                        {/*<Image src='/logo.png'/> */}
                        Login
                    </Header>
                    <Form size="large">
                        <Segment stacked>

                            <Form.Input
                                fluid
                                icon="user"
                                iconPosition="left"
                                placeholder="E-mail address"
                                type="email"
                                name="email"
                                value={this.state.email}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                icon="lock"
                                iconPosition="left"
                                placeholder="Password"
                                type="password"
                                name="password"
                                value={this.state.password}
                                onChange={this.handle_change}
                            />
                            <Button
                                color="blue"
                                fluid size="large"
                                name="login_button"
                                disabled={
                                    !this.state.email || !this.state.password
                                }
                            >
                                Login
                            </Button>
                        </Segment>
                    </Form>
                    <Message>
                        New to us?{" "}
                        <a
                            id="signup_link"
                            href="#" onClick={() => this.props.handleRegisterClicked('signup')}>
                            Sign Up
                        </a>
                    </Message>
                    <Message>
                        Forgot your password?{" "}
                        <a
                            id="password_reset_link"
                            href="#" onClick={() => {window.location = `${baseRoute}/password/reset`;}}>
                            Reset Password
                        </a>
                    </Message>
                </Grid.Column>
            </Grid>
        );
    }
}

export default LoginForm;

/**
 * Setting up the properties types
 * @type {{handle_login: function, handleRegisterClicked: function}}
 */
LoginForm.propTypes = {
    // Getting the handle_login function
    handle_login: PropTypes.func.isRequired,

    // Getting the going back to signup form function
    handleRegisterClicked: PropTypes.func.isRequired
};
