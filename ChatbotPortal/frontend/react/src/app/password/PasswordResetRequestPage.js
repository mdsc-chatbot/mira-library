/**
 * @file: PasswordResetRequestPage.js
 * @summary: Renders the form that allows the user to request for password through typing their email
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
import {Button, Form, Grid, Header, Message, Segment} from "semantic-ui-react";
import axios from "axios";
import { SecurityContext } from "../contexts/SecurityContext";

/**
 * This class sends the password change request to a respective email
 */
class PasswordResetRequestPage extends React.Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            email: "",
            email_sent: false
        };
    }

    /**
     * This function sends the password change request email by calling the backend API
     * @param e = event
     * @param emailFormData = Data procured from the email form
     */
    handle_email = (e, emailFormData) => {
        const url = `/chatbotportal/authentication/password/reset/`;

        axios
            .post(url, emailFormData)
            .then(
                response => {
                    console.log(response);
                    this.setState({
                        email_sent: true
                    });
                },
                error => {
                    console.log(error);
                }
            );
    };

    /**
     * This function handles the changes that happens to the email form
     * @param e = event
     */
    handle_email_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevstate => {
            const newState = { ...prevstate };
            newState[name] = value;
            return newState;
        });
    };

    render() {
        return (
            <Grid
                onSubmit={e => this.handle_email(e, this.state)}
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
                                icon="user"
                                iconPosition="left"
                                type="email"
                                name="email"
                                placeholder="E-mail address"
                                value={this.state.email}
                                onChange={this.handle_email_change}
                            />
                            <Button
                                color="blue"
                                fluid
                                size="large"
                                name="password_reset_button"
                                disabled={!this.state.email}
                            >
                                Request
                            </Button>
                            <Message
                                content={
                                    this.state.email_sent
                                        ? "An email is sent with a password change link, Please check your email."
                                        : "Email is not sent yet."
                                }
                            />
                        </Segment>
                    </Form>
                </Grid.Column>
            </Grid>
        );
    }
}

export default PasswordResetRequestPage;