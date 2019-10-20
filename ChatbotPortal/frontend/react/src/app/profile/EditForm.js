import React from 'react';
import PropTypes from 'prop-types';
import {Button, Form, Grid, Header, Segment} from "semantic-ui-react";
import {SecurityContext} from '../security/SecurityContext';

class EditForm extends React.Component {

    static contextType = SecurityContext;

    constructor(props) {
		super(props);
		this.state = {
			logged_in: '',
			id: '',
			email: '',
            first_name: '',
            last_name: '',
			is_edited: false,
		};
	}

    componentDidMount() {
        if (this.context.security.logged_in) {
            // fetch('http://localhost:8000/signup/current_user/', {
            //     headers: {
            //         Authorization: `JWT ${localStorage.getItem('token')}`
            //     }
            // })
            //     .then(res => res.json())
            //     .then(json => {
            //         this.setState({
            //             id: json.id,
            //             email: json.email,
            //             first_name: json.first_name,
            //             last_name: json.last_name
            //         });
            //     });
            this.setState({
                logged_in: this.context.security.logged_in,
                id: this.context.security.id,
                email: this.context.security.email,
                first_name: this.context.security.first_name,
                last_name: this.context.security.last_name,
                is_edited: false,
            })
        }
    }

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
            <Grid onSubmit={e => this.props.handle_edit(e, this.state)}
                  textAlign='center'
                  style={{height: '100vh'}}
                  verticalAlign='middle'>
                <Grid.Column style={{maxWidth: 450}}>
                    <Header as='h2' color='teal' textAlign='center'>
                        {/*<Image src='/logo.png'/> */}
                        Edit Your Account
                    </Header>
                    <Form size='large'>
                        <Segment stacked>
                            <Form.Input fluid
                                placeholder='First Name'
                                name='first_name'
                                value={this.state.first_name}
                                onChange={this.handle_change}
                            />
                            <Form.Input fluid
                                placeholder='Last Name'
                                name='last_name'
                                value={this.state.last_name}
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

                            <Button
                                color='teal'
                                fluid size='large'
                                onClick={this.props.is_edited}
                            >
                                Save
                            </Button>
                        </Segment>
                    </Form>
                </Grid.Column>
            </Grid>
        );
    }
}

export default EditForm;

EditForm.propTypes = {
    handle_edit: PropTypes.func.isRequired,
    is_edited: PropTypes.func.isRequired
};