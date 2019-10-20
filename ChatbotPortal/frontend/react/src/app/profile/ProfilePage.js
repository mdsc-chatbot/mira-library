import React, {Component} from 'react';
import Profile from "./Profile";
import {SecurityContext} from '../security/SecurityContext';
import Nav from "../authentication/Nav";
import LoginForm from "../authentication/LoginForm";
import {Header, Icon, Divider, Table, Message, Container, Input, Form, Button} from 'semantic-ui-react'
import Image from "semantic-ui-react/dist/commonjs/elements/Image";
import {unstable_renderSubtreeIntoContainer} from "react-dom";
// import styles from './ProfilePage.css'
import EditForm from "./EditForm";


class ProfilePage extends Component {

    static contextType = SecurityContext;

    constructor(props){
        super(props);
        this.state = {
            token: '',
            displayed_form: 'edit',
            logged_in: '',
            id: '',
            email: '',
            first_name: '',
            last_name: '',
            is_edited: false,
            password:''
        };
    }

    componentDidMount() {
        if (this.context.security.logged_in) {

            this.setState({
                logged_in: this.context.security.logged_in,
                token: this.context.security.token,
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

    handle_edit = (e, data, setSecurity) => {
        e.preventDefault();
        fetch(`http://localhost:8000/signup/${this.state.id}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(json => {
                setSecurity({
                    logged_in: true,
                    id: json.id,
                    email: json.email,
                    first_name: json.first_name,
                    last_name: json.last_name
                });
                this.setState({
                    logged_in: true,
                    id: json.id,
                    email: json.email,
                    first_name: json.first_name,
                    last_name: json.last_name,
                });
            });
    };

    updateURL = pk => {
        this.setState({
            url: `http://localhost:8000/${pk}/update/`
        })
    };

    is_edited = () => {
        this.setState({
            edited: true
        });
    };

    render() {
        return (
            <React.Fragment>
                <Container>
                    <div>
                        <Divider horizontal>
                            <Header as='h4'>
                                <Icon name='user' />
                                My Profile
                            </Header>
                        </Divider>

                        <SecurityContext.Consumer>
                            {(securityContext) => (
                                <React.Fragment>
                                    <Form onSubmit={e => this.handle_edit(e, this.state)}>
                                        <Table definition color='blue' onSubmit={this.props.handle_edit}>
                                            {securityContext.security.logged_in ?
                                                <Table.Body>
                                                    <Table.Row>
                                                        <Table.Cell width={3}>Profile Picture</Table.Cell>
                                                        <Table.Cell>
                                                            <Image src='https://www.iconsdb.com/icons/download/color/4AFFFF/user-512.png' size='small' />
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
                                                        <Table.Cell><Form.Input name='first_name' onChange={this.handle_change} value={this.state.first_name} /></Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell >Last Name</Table.Cell>
                                                        <Table.Cell><Form.Input name='last_name' onChange={this.handle_change} value={this.state.last_name} />
                                                        </Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Status</Table.Cell>
                                                        <Table.Cell>Newbie</Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Submissions</Table.Cell>
                                                        <Table.Cell >0</Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Points</Table.Cell>
                                                        <Table.Cell >0</Table.Cell>
                                                    </Table.Row>
                                                    <Table.Row>
                                                        <Table.Cell>Password</Table.Cell>
                                                        <Table.Cell ><Form.Input name='password' onChange={this.handle_change} value={this.state.password} /></Table.Cell>
                                                    </Table.Row>
                                                </Table.Body>
                                                : null}
                                        </Table>

                                        {securityContext.security.logged_in ? (
                                            <Button
                                                color='teal'
                                                fluid size='large'
                                                onClick={this.is_edited}>Save
                                            </Button>
                                        ) : null}
                                    </Form>
                                    {!securityContext.security.logged_in ? (<Message icon error>
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
