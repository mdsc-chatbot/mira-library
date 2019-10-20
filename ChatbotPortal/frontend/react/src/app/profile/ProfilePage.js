import React, {Component} from 'react';
import Profile from "./Profile";
import {SecurityContext} from '../security/SecurityContext';
import Nav from "../authentication/Nav";
import LoginForm from "../authentication/LoginForm";
import { Header, Icon, Divider, Table, Message, Container, Input } from 'semantic-ui-react'
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
            url: ''
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
                                <div>
                                    <Table definition color='blue'>
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
                                                        <Input defaultValue={securityContext.security.email} />
                                                    </Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell>First Name</Table.Cell>
                                                    <Table.Cell><Input  defaultValue={securityContext.security.first_name} /></Table.Cell>
                                                </Table.Row>
                                                <Table.Row>
                                                    <Table.Cell >Last Name</Table.Cell>
                                                    <Table.Cell><Input defaultValue={securityContext.security.last_name} />
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
                                            </Table.Body>
                                            :
                                            <Message icon error>
                                                <Icon name='circle notched' loading/>
                                                <Message.Content>
                                                    <Message.Header>Nothing to show here!</Message.Header>
                                                    Log in and try again?
                                                </Message.Content>
                                            </Message>}
                                    </Table>
                                </div>

                            )}
                        </SecurityContext.Consumer>
                    </div>
                </Container>
                <div>
                    <SecurityContext.Consumer>
                        {(securityContext) => (
                            <div>
                                <h3>
                                    {securityContext.security.logged_in
                                        ? 	`Email: ${securityContext.security.email} '\n'
                                	 First Name: ${securityContext.security.first_name} '\n'
                                	 Last Name: ${securityContext.security.last_name} '\n'
                                	 Affiliation: ${securityContext.security.affiliation} '\n'
                                	 Active: ${securityContext.security.active} '\n'
                                	 Staff: ${securityContext.security.staff} '\n'
                                	 Admin: ${securityContext.security.admin}`
                                        : 'No Security Context'}
                                </h3>
                            </div>
                        )}
                    </SecurityContext.Consumer>
                </div>
            </React.Fragment>
        );
    }
}

export default ProfilePage;
