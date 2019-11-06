import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Card, Checkbox, Container, Form, Icon, Image, Label, Segment} from 'semantic-ui-react';
import styles from "../profile/ProfilePage.css";

class UserPage extends Component {
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
            // id: '',
            first_name: '',
            last_name: '',
            // email: '',
            is_active: '',
            is_reviewer: '',
            is_staff: '',
            // profile_picture: ''
        };
    };

    componentDidMount() {
        this.setState({
            // id: this.props.rowData.id,
            first_name: this.props.rowData.first_name,
            last_name: this.props.rowData.last_name,
            // email: this.props.rowData.email,
            is_active: this.props.rowData.is_active,
            is_reviewer: this.props.rowData.is_reviewer,
            is_staff: this.props.rowData.is_staff,
            // profile_picture: this.props.rowData.profile_picture
        })
    };

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevState => {
            const newState = {...prevState};
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
            .put(`http://127.0.0.1:8000/authentication/auth/${this.props.rowData.id}/update/`, editedData, {headers: options})
            .then(
                response => {
                    this.setState({
                        first_name: response.data['first_name'],
                        last_name: response.data['last_name'],
                        is_edited: true,
                    });
                },
                error => {
                    console.log(error);
                }
            );
    };

    /**
     * This function handles the delete operation
     * @param e : event
     */
    handle_delete = (e) => {
        e.preventDefault();

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        /**
         * Perform a delete request for deleting the user.
         * Upon successful response, returns 204 not found.
         * Otherwise, send an error is thrown."
         */
        axios
            .delete(`http://127.0.0.1:8000/authentication/auth/delete/${this.state.id}/`, {headers: options})
            .then(
                response => {
                    console.log(response.status)
                },
                error => {
                    console.log(error);
                }
            );

    };

    /**
     * This function handles the checkbox change options, and set the state accordingly
     * @param e : event
     * @param name : name of the checkbox field
     * @param value : value of the checkbox field
     */
    handle_toggle = (e, {name, value}) => {
        this.setState(prevState => {
            const newState = {...prevState};
            newState[name] = !value;
            return newState;
        });
    };

    /**
     * This renders the ProfileForm
     * @returns {React.Fragment}
     */
    render() {
        return (
            <React.Fragment>
                <Container>
                    <Form className={styles.centeredForm}>
                        <Segment className={styles.segmentBackground}>
                            <Label
                                size='big'
                                as='h1'
                                icon='user'
                                color='red'
                                content='Sample Profile'
                                ribbon>
                            </Label>
                            <Card className={styles.cardBackground}
                                  fluid
                                  centered
                            >

                                {this.props.rowData.profile_picture ?
                                    <Image
                                        src={`/static/${this.props.rowData.profile_picture.split('/')[this.props.rowData.profile_picture.split('/').length - 1]}`}
                                        wrapped ui={true}
                                    />
                                    : null}

                                <Card.Content>
                                    <Card.Header>
                                        <Form.Group widths='equal'>
                                            <Form.Input
                                                className={styles.fixedInputHeight}
                                                fluid
                                                label='First name'
                                                name='first_name'
                                                onChange={this.handle_change}
                                                value={this.state.first_name}
                                            />
                                            <Form.Input
                                                className={styles.fixedInputHeight}
                                                fluid
                                                label='Last name'
                                                name='last_name'
                                                onChange={this.handle_change}
                                                value={this.state.last_name}
                                            />
                                        </Form.Group>
                                    </Card.Header>
                                </Card.Content>

                                <Card.Content extra>
                                    <h3>
                                        <Icon color='red' name='mail'/>
                                        {this.state.email}
                                    </h3>
                                </Card.Content>

                                <Card.Content extra>
                                    <h3>
                                        <Icon color='red' name='certificate'/>
                                        Newbie
                                    </h3>
                                </Card.Content>

                                <Card.Content extra>
                                    <h3>
                                        <Icon color='red' name='pencil alternate'/>
                                        # Submissions = 25
                                    </h3>
                                </Card.Content>

                                <Card.Content extra>
                                    <h3>
                                        <Icon color='red' name='trophy'/>
                                        Points = 56
                                    </h3>
                                </Card.Content>

                                <Card.Content extra>
                                    <Segment.Group horizontal>
                                        <Segment color='red'>
                                            <Checkbox
                                                checked={this.state.is_active}
                                                label='Active'
                                                name='is_active'
                                                value={this.state.is_active}
                                                onChange={this.handle_toggle}
                                                slider
                                            />
                                        </Segment>
                                        <Segment color='red'>
                                            <Checkbox
                                                checked={this.state.is_reviewer}
                                                label='Reviewer'
                                                name='is_reviewer'
                                                value={this.state.is_reviewer}
                                                onChange={this.handle_toggle}
                                                slider
                                            />
                                        </Segment>
                                        <Segment color='red'>
                                            <Checkbox
                                                checked={this.state.is_staff}
                                                label='Staff'
                                                name='is_staff'
                                                value={this.state.is_staff}
                                                onChange={this.handle_toggle}
                                                slider
                                            />
                                        </Segment>
                                    </Segment.Group>
                                </Card.Content>

                                <Button
                                    color='green'
                                    fluid
                                    size='huge'
                                    onClick={e => this.handle_edit(e, this.state)}
                                >
                                    <Icon name='save'/>Save
                                </Button>
                                <Button
                                    color='red'
                                    fluid
                                    size='huge'
                                    onClick={e => this.handle_delete(e)}
                                >
                                    <Icon name='delete'/>Delete User
                                </Button>
                            </Card>
                        </Segment>
                    </Form>
                </Container>
            </React.Fragment>
        );
    }
}

export default UserPage;
