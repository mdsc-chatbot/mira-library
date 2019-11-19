import React from "react";
import {SecurityContext} from "../security/SecurityContext";
import {Button, Container, Form, Grid, Header, Segment} from "semantic-ui-react";
import axios from "axios";
import {baseRoute} from "../App";

class PasswordChangeForm extends React.Component {
    /**
     * This class renders the profile information
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    /**
     * This construct initializes the state.
     * @param props
     */
    constructor(props) {
        super(props);
        /**
         * The state of the component
         * @type {{password: string, new_password2: string, password_matched: boolean}}
         */
        this.state = {
            'password': '',
            'new_password2': '',
            'password_matched': false
        }
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

            const url = `/chatbotportal/authentication/${this.context.security.id}/update/password/`;

            // Defining header and content-type for accessing authenticated information
            const options = {
                'Authorization': `Bearer ${this.context.security.token}`,
                // "Content-Type":"multipart/form-data"
                'Content-Type': 'application/json',
            };

            axios
                .put(url, passwordFormData, {headers: options})
                .then(
                    response => {
                        console.log(response);
                        // Upon successful changing of password, redirect the user to the login page
                        // window.location = `${baseRoute}`;
                    },
                    error => {
                        console.log(error)
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
            const newState = {...prevstate};
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
            const newState = {...prevstate};
            newState[name] = value;
            return newState;
        });

        /**
         * Matching both the field to enable reset call
         */
        if (value !== null && value === this.state.password) {
            this.setState({
                'password_matched': true
            })
        } else {
            this.setState({
                'password_matched': false
            })
        }
    };

    render() {
        return (
            <React.Fragment>
                <Container>
                    <SecurityContext.Consumer>
                        {(securityContext) => (
                            <Grid
                                onSubmit={e => this.handle_password(e, this.state)}
                                textAlign="center"
                                style={{height: "100vh"}}
                                verticalAlign="middle"
                            >
                                {securityContext.security.is_logged_in ?
                                    <Grid.Column style={{maxWidth: 450}}>
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
                                                    placeholder="Password"
                                                    type="password"
                                                    name="password"
                                                    value={this.state.password}
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
                                                <Button color="blue" fluid size="large" name="login_button">
                                                    {this.state.password_matched ? "Click" : "Password does not match"}
                                                </Button>
                                            </Segment>
                                        </Form>
                                    </Grid.Column>
                                    : () => {
                                        // Upon successful changing of password, redirect the user to the login page
                                        window.location = `${baseRoute}`;
                                    }}
                            </Grid>
                        )}
                    </SecurityContext.Consumer>
                </Container>
            </React.Fragment>
        )

    }
}

export default PasswordChangeForm;