import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Container, Divider, Form, Header, Icon, Message, Table} from 'semantic-ui-react'
import Image from "semantic-ui-react/dist/commonjs/elements/Image";


class ProfilePage extends Component {
    /**
     * This class renders the profile information
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    BASE_AUTH_URL = 'http://127.0.0.1:8000/authentication/auth/';


    constructor(props) {
        /**
         * This constructor sets up the primary state for the props
         */
        super(props);
        this.state = {
            is_logged_in: '',
            is_edited: '',
            first_name: '',
            last_name: ''
        };
    };

    componentDidMount() {
        /**
         * Upon mounting the component, it checks the login state from the security context,
         * if the login state is gone due to refresh, then the current user is retrieved,
         * and required information is stored in the props.
         */
        if (!this.context.security.is_logged_in) {
            axios
                .get(this.BASE_AUTH_URL + 'currentuser/')
                .then(
                    response => {
                        if (response.data !== '') {
                            this.setState({
                                first_name: response.data['first_name'],
                                last_name: response.data['last_name'],
                                is_logged_in: true,
                                is_edited: false
                            })
                        } else {
                            this.setState({
                                is_logged_in: false
                            });
                        }
                    },
                    error => {
                        console.log(error);
                    }
                );
        } else {
            /**
             * If the context says that the user is already logged in,
             * then set the props using the security context data
             */
            this.setState({
                is_logged_in: this.context.security.is_logged_in,
                is_edited: false,
                first_name: this.context.security.first_name,
                last_name: this.context.security.last_name
            });
        }
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

    /**
     * This function handles the overall edit operations
     * @param e : event
     * @param editedData : data from the EditForm upon submission
     */
    handle_edit = (e, editedData) => {
        e.preventDefault();

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        /**
         * Perform a put request for edit.
         * Upon successful response, set the security context and component props with response data.
         * Otherwise, send an error is thrown."
         */
        axios
            .put(this.BASE_AUTH_URL + this.context.security.id + '/update/', editedData, {headers: options})
            .then(
                response => {
                    this.setState({
                        first_name: response.data['first_name'],
                        last_name: response.data['last_name'],
                        is_edited: true,
                    });
                    this.context.security.first_name = this.state.first_name;
                    this.context.security.last_name = this.state.first_name;
                    console.log(this.context.security)
                },
                error => {
                    console.log(error);
                }
            );
    };

    /**
     * This renders the ProfileForm
     * @returns {React.Fragment}
     */
    render() {
        return (
            <React.Fragment>
                <Container>
                    <div>
                        <Divider horizontal>
                            <Header as='h4'>
                                <Icon name='user'/>
                                My Profile
                            </Header>
                        </Divider>
                        <SecurityContext.Consumer>
                            {(securityContext) => (
                                <React.Fragment>
                                    <Form onSubmit={e => this.handle_edit(e, this.state)}>
                                        <Table definition color='blue' onSubmit={this.props.handle_edit}>
                                            {securityContext.security.is_logged_in ?
                                                <Table.Body>
                                                    <Table.Row>
                                                        <Table.Cell width={3}>Profile Picture</Table.Cell>
                                                        <Table.Cell>
                                                            <Image
                                                                src='https://www.iconsdb.com/icons/download/color/4AFFFF/user-512.png'
                                                                size='small'/>
                                                        </Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Email</Table.Cell>
                                                        <Table.Cell>
                                                            {/*<Input name='email' onChange={this.handle_change} defaultValue={securityContext.security.email} />*/}
                                                            {securityContext.security.email}
                                                        </Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>First Name</Table.Cell>
                                                        <Table.Cell><Form.Input name='first_name'
                                                                                onChange={this.handle_change}
                                                                                value={this.state.first_name}/></Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Last Name</Table.Cell>
                                                        <Table.Cell><Form.Input name='last_name'
                                                                                onChange={this.handle_change}
                                                                                value={this.state.last_name}/></Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Status</Table.Cell>
                                                        <Table.Cell>Newbie</Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Submissions</Table.Cell>
                                                        <Table.Cell>0</Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Points</Table.Cell>
                                                        <Table.Cell>0</Table.Cell>
                                                    </Table.Row>
                                                </Table.Body>
                                                : null}
                                        </Table>

                                        {securityContext.security.is_logged_in ? (
                                            <Button
                                                color='blue'
                                                fluid size='large'>Save
                                            </Button>
                                        ) : null}
                                    </Form>
                                    {!securityContext.security.is_logged_in ? (<Message icon error>
                                            <Icon name='circle notched' loading/>
                                            <Message.Content>
                                                <Message.Header>Nothing to show here!</Message.Header>
                                                Log in and try again?
                                            </Message.Content>
                                        </Message>)
                                        : null}
                                </React.Fragment>
                            )}
                        </SecurityContext.Consumer>
                    </div>
                </Container>
            </React.Fragment>
        );
    }
}

export default ProfilePage;
