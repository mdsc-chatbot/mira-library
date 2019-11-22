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
            .post(url, emailFormData, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
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