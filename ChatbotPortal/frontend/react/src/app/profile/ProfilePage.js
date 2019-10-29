import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Container, Form, Icon, Card, Image, Segment, Label} from 'semantic-ui-react'


const styles = {
    center: {
        marginLeft: "auto",
        marginRight: "auto",
        width:'400px',
        border:'1px'
    }
}

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
                    this.context.security.last_name = this.state.last_name;
                    console.log(this.context.security)
                    console.log("Saved Changes")
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
                    <div className={styles.center}>
                        <SecurityContext.Consumer>
                            {(securityContext) => (
                                <React.Fragment className={styles.center}>
                                    <Form style={{ width:"50%"}} onSubmit={e => this.handle_edit(e, this.state)}>
                                        <Segment style={{ backgroundColor:"PaleGreen"}}>
                                            <Label
                                                size='big'
                                                as='h1'
                                                icon='user'
                                                color='blue'
                                                content='My Profile'
                                                ribbon>
                                            </Label>
                                            {securityContext.security.is_logged_in ?
                                                <Card style={{ backgroundColor: 'lavender'}} fluid centered onSubmit={this.props.handle_edit}>
                                                    <Image src='https://react.semantic-ui.com/images/avatar/large/daniel.jpg' wrapped ui={true} />
                                                    <Card.Content>
                                                        <Card.Header>

                                                            <Form.Group widths='equal'>

                                                                <Form.Input
                                                                    style={{height:'38px'}}
                                                                    fluid
                                                                    label='First name'
                                                                    name='first_name'
                                                                    onChange={this.handle_change}
                                                                    value={this.state.first_name}
                                                                />
                                                                <Form.Input
                                                                    style={{height:'38px'}}
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
                                                        {/*<h3 style={{ color: 'green' }}>*/}
                                                        <h3>
                                                            <Icon color='blue' name='mail'/>
                                                            {securityContext.security.email}
                                                        </h3>
                                                    </Card.Content>

                                                    <Card.Content extra>
                                                        <h3>
                                                            <Icon color='blue' name='certificate'/>
                                                            Newbie
                                                        </h3>
                                                    </Card.Content>

                                                    <Card.Content extra>
                                                        <h3>
                                                            <Icon color='blue' name='pencil alternate'/>
                                                            # Submissions = 25
                                                        </h3>
                                                    </Card.Content>

                                                    <Card.Content extra>
                                                        <h3>
                                                            <Icon color='blue' name='trophy'/>
                                                            Points = 56
                                                        </h3>
                                                    </Card.Content>


                                                        <Button
                                                            color='blue'
                                                            fluid
                                                            size='huge'
                                                        >
                                                           <Icon name='sync' />Save Changes
                                                        </Button>


                                                </Card>
                                                : null}
                                        </Segment>
                                    </Form>

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
