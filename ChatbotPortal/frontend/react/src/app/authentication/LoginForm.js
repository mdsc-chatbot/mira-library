import React from 'react';
import PropTypes from 'prop-types';
import {Button, Form, Grid, Header, Image, Message, Segment} from 'semantic-ui-react'

class LoginForm extends React.Component {
    state = {
        email: '',
        password: ''
    };

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

            <Grid onSubmit={e => this.props.handle_login(e, this.state)} textAlign='center' style={{height: '100vh'}}
                  verticalAlign='middle'>
                <Grid.Column style={{maxWidth: 450}}>
                    <Header as='h2' color='teal' textAlign='center'>
                        {/*<Image src='/logo.png'/> */}
                        Log-in to your account
                    </Header>
                    <Form size='large'>
                        <Segment stacked>
                            <Form.Input
                                fluid icon='user'
                                iconPosition='left'
                                placeholder='E-mail address'
                                name='email'
                                value={this.state.email}
                                onChange={this.handle_change}
                            />
                            <Form.Input
                                fluid
                                icon='lock'
                                iconPosition='left'
                                placeholder='Password'
                                type='password'
                                name='password'
                                value={this.state.password}
                                onChange={this.handle_change}
                            />
                            <Button color='teal' fluid size='large'>
                                Login
                            </Button>
                        </Segment>
                    </Form>
                    <Message>
                        New to us? <a href='#' onClick={this.props.handleRegisterClicked}>Sign Up</a>
                    </Message>
                </Grid.Column>
            </Grid>
        );
    }
}

export default LoginForm;

LoginForm.propTypes = {
    handle_login: PropTypes.func.isRequired,
    handleRegisterClicked: PropTypes.func.isRequired,
};