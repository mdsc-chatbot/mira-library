import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Container, Form, Icon, Card, Image, Segment, Label, Checkbox} from 'semantic-ui-react';
import styles from "./ProfilePage.css";

class ProfilePage extends Component {
    /**
     * This class renders the profile information
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

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
                .get('/chatbotportal/authentication/currentuser/')
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
            .put(`/chatbotportal/authentication/${this.context.security.id}/update/`, editedData, {headers: options})
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
                    <SecurityContext.Consumer>
                        {(securityContext) => (

                            <Form className={styles.centeredForm} onSubmit={e => this.handle_edit(e, this.state)}>
                                <Segment className={styles.segmentBackground}>
                                    <Label
                                        size='big'
                                        as='h1'
                                        icon='user'
                                        color='red'
                                        content='Sample Profile'
                                        ribbon>
                                    </Label>
                                    {securityContext.security.is_logged_in ?
                                        <Card className={styles.cardBackground} fluid centered onSubmit={this.props.handle_edit}>
                                            <Image src='https://react.semantic-ui.com/images/avatar/large/daniel.jpg' wrapped ui={true} />
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
                                                {/*<h3 style={{ color: 'green' }}>*/}
                                                <h3>
                                                    <Icon color='red' name='mail'/>
                                                    {securityContext.security.email}
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
                                                        <Checkbox label='Staff' slider />
                                                    </Segment>
                                                    <Segment color='red'>
                                                        <Checkbox label='Reviewer' slider />
                                                    </Segment>
                                                </Segment.Group>
                                            </Card.Content>


                                            <Button
                                                color='red'
                                                fluid
                                                size='huge'
                                            >
                                                <Icon name='delete' />Delete User
                                            </Button>


                                        </Card>
                                        : null}
                                </Segment>
                            </Form>

                        )}
                    </SecurityContext.Consumer>
                </Container>
            </React.Fragment>
        );
    }
}

export default ProfilePage;
