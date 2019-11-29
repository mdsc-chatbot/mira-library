/**
 * @file: Signup.js
 * @summary: The user interactive form component for signup
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
import { Button, Form, Grid, Header, Message, Segment} from "semantic-ui-react";
import TermsOfService from "./TermsOfService";

class SignupForm extends React.Component {
    /**
     * This class manages the Signup form
     * @type {{
     *      password: string,
     *      affiliation: string,
     *      last_name: string,
     *      password2: string,
     *      consent: boolean,
     *      first_name: string,
     *      password_matched: boolean,
     *      is_validated: boolean,
     *      email: string}}
     */
    state = {
        email: "",
        first_name: "",
        last_name: "",
        affiliation: "",
        password: "",
        password2: '',
        password_matched: false,
        consent:false,
        is_validated:true
    };
    baseState = this.state;

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

    /**
     * Set state for consent checkbox
     */
    handle_change_consent = () => {
        this.setState(({ consent }) => ({ consent: !consent }));
    };

    /**
     * Sign Up Form Validation Requirements: 
     * - consent checkbox must be checked
     * - email must not be the same (TODO)
     * - some field must not be empty (TODO)
     */
    validate_signup_form = (e, state) =>{
        if (state.consent === false){
            this.setState({is_validated:false});
        }else{
            this.props.handle_signup(e, state);
            this.setState(this.baseState);
        }
    };

    render() {
        return (
            <Grid
                onSubmit={e => this.validate_signup_form(e, this.state)}
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

                            {
                                this.state.is_validated ? (
                                    <Form.Checkbox
                                        fluid
                                        label={<label>I consent and agree to the <TermsOfService /> </label>}
                                        name="consent"
                                        checked={this.state.consent}
                                        onChange={this.handle_change_consent}
                                    />
                                ) : (
                                    <Form.Checkbox
                                        fluid
                                        label={<label>I consent to the <TermsOfService /> </label>}
                                        name="consent"
                                        checked={this.state.consent}
                                        onChange={this.handle_change_consent}
                                        error={{
                                            content: 'Please read and consent to the Terms of Service',
                                            pointing: 'left',
                                        }}
                                    />
                                )
                            }

                            <Button
                                color="blue"
                                fluid size="large"
                                disabled={
                                    !this.state.email ||
                                    !this.state.consent ||
                                    !(this.state.password.length >= 8 && this.state.password_matched)
                                }
                            >Signup</Button>
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
