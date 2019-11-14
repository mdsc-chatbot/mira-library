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
                        <a href="#" onClick={() => {window.location = `${baseRoute}/password/reset`;}}>
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
