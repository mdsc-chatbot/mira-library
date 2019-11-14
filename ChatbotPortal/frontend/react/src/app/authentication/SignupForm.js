import React from "react";
import PropTypes from "prop-types";
import {Button, Form, FormField, Grid, Header, Message, Segment} from "semantic-ui-react";

class SignupForm extends React.Component {
    /**
     * This class manages the Signup form
     * @type {
     *      {
     *          password: string,
     *          affiliation: string,
     *          last_name: string,
     *          first_name: string,
     *          email: string}
     *      }
     */
    state = {
        email: "",
        first_name: "",
        last_name: "",
        affiliation: "",
        password: "",
        password2: '',
        password_matched: false
    };

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e : event
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
                password_matched: true
            })
        } else {
            this.setState({
                password_matched: false
            })
        }
    };

    render() {
        return (
            <Grid
                onSubmit={e => this.props.handle_signup(e, this.state)}
                textAlign="center"
                style={{height: "100vh"}}
                verticalAlign="middle"
            >
                <Grid.Column style={{maxWidth: 450}}>
                    <Header as="h2" color="blue" textAlign="center">
                        {/*<Image src='/logo.png'/> */}
                        Create your account
                    </Header>
                    <Form size="large">
                        <Segment stacked>
                            <Form.Input
                                fluid
                                placeholder="First Name"
                                name="first_name"
                                value={this.state.first_name}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                placeholder="Last Name"
                                name="last_name"
                                value={this.state.last_name}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                icon="user"
                                type="email"
                                iconPosition="left"
                                placeholder="E-mail address * (Required)"
                                name="email"
                                value={this.state.email}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                placeholder="Affiliation"
                                name="affiliation"
                                value={this.state.affiliation}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                icon="lock"
                                iconPosition="left"
                                placeholder="Password * (Required)"
                                type="password"
                                name="password"
                                value={this.state.password}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                icon="lock"
                                iconPosition="left"
                                placeholder="Confirm Password * (Required)"
                                type="password"
                                name="password2"
                                value={this.state.password2}
                                onChange={this.handle_password2}
                            />
                            <Button

                                color="blue"
                                fluid size="large"
                                disabled={!this.state.email || !(this.state.password.length >= 8 && this.state.password_matched)}
                            >
                                Signup
                            </Button>
                        </Segment>
                    </Form>
                    <Message>
                        Already have an account?{" "}
                        <a
                            href="#"
                            onClick={() => this.props.handleLoginClicked('signup')}>
                            Login
                        </a>
                    </Message>
                </Grid.Column>
            </Grid>
        );
    }
}

export default SignupForm;

/**
 * Setting up the properties types
 * @type {{handle_signup: function, handleLoginClicked: function}}
 */
SignupForm.propTypes = {
    // Getting the handle_signup function
    handle_signup: PropTypes.func.isRequired,

    // Getting the going back to login form function
    handleLoginClicked: PropTypes.func.isRequired
};
