import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Grid, Header, Message, Segment} from "semantic-ui-react";
import TermsOfService from "./TermsOfService";

class SignupForm extends React.Component {
    /**
     * This class manages the Signup form
     * @type {
     *      {
     *          password: string,
     *          affiliation: string,
     *          last_name: string,
     *          first_name: string,
     *          email: string,
     *          consent: checkbox,
     *          is_validated: boolean}
     *      }
     */
    state = {
        email: "",
        first_name: "",
        last_name: "",
        affiliation: "",
        password: "",
        consent:false,
        is_validated:true,
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
     * Set state for consent checkbox
     */
    handle_change_consent = () => {
        this.setState(({ consent }) => ({ consent: !consent }));
    }

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
    }

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
                                iconPosition="left"
                                placeholder="E-mail address"
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
                                placeholder="Password"
                                type="password"
                                name="password"
                                value={this.state.password}
                                onChange={this.handle_change}
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

                            <Button color="blue" fluid size="large">
                                Signup
                            </Button>
                        </Segment>
                    </Form>
                    <Message>
                        Already have an account?{" "}
                        <a href="#" onClick={() => this.props.handleLoginClicked('signup')}>
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
