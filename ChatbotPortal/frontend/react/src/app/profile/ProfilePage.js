import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Container, Form, Icon, Card, Image, Segment, Label, Input} from 'semantic-ui-react';
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
            is_logged_in: false,
            is_edited: '',
            first_name: '',
            last_name: '',
            profile_picture: null,
            submissions:'',
            points:'',
        };
    };

    componentDidMount() {
        this.updateStateFromSecurityContext();
    }

    componentDidUpdate() {
        this.updateStateFromSecurityContext();

    }

    updateStateFromSecurityContext =() => {
        if (this.state.is_logged_in === false && this.context.security && this.context.security.is_logged_in) {
            this.setState({
                is_logged_in: this.context.security.is_logged_in,
                is_edited: false,
                first_name: this.context.security.first_name,
                last_name: this.context.security.last_name,
                profile_picture: this.context.security.profile_picture,
                submissions: this.context.security.submissions,
                points: this.context.security.points,
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

    handleImageChange = event => {
        this.setState({
            // [event.nativeEvent.target.name]: event.nativeEvent.target.files[0],
            // imagePath: event.nativeEvent.target.value
            imagePath: event.target.files[0]
        })
    };


    saveFunction = () => {
        alert("Your changes were saved!");
    };

    cancelFunction = () => {
        alert("No changes were saved!");
    };

    deleteFunction = () => {
        alert("A request has been sent to the admin!");
    };

    /**
     * This function handles the overall edit operations
     * @param e : event
     * @param editedData : data from the EditForm upon submission
     */
    handle_edit = (e, editedData) => {
        e.preventDefault();
        let formData = new FormData();
        if (this.state.imagePath) formData.append('profile_picture', this.state.imagePath);
        formData.append('first_name', this.state.first_name);
        formData.append('last_name', this.state.last_name);
        // Object.values(editedData).forEach((formField) => {
        //     if (formField[0] !== 'imagePath') {
        //         formData.append(formField[2], formField[3]);
        //     }
        // });

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Authorization': `Bearer ${this.context.security.token}`,
            // "Content-Type":"multipart/form-data"
            'Content-Type': 'application/json',
        };

        /**
         * Perform a put request for edit.
         * Upon successful response, set the security context and component props with response data.
         * Otherwise, send an error is thrown."
         */
        axios
            .put(`/chatbotportal/authentication/${this.context.security.id}/update/`, formData, {headers: options})
            .then(
                response => {
                    console.log(response.data);
                    this.setState({
                        first_name: response.data['first_name'],
                        last_name: response.data['last_name'],
                        profile_picture:response.data['profile_picture'],
                        is_edited: true,
                    });
                    this.context.security.first_name = this.state.first_name;
                    this.context.security.last_name = this.state.last_name;
                    this.context.security.profile_picture = this.state.profile_picture;
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
                                <Segment>
                                    <Label
                                        size='big'
                                        as='h1'
                                        icon='user'
                                        color='blue'
                                        content='My Profile'
                                        ribbon>
                                    </Label>
                                    {securityContext.security.is_logged_in ?
                                        <Card fluid centered onSubmit={this.props.handle_edit}>
                                            {this.state.profile_picture ? (
                                                <Image src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`} />
                                            ) : null}
                                            <Form.Input type='file' accept="image/png, image/jpeg" id='profile_picture' name='profile_picture' onChange={this.handleImageChange}/>
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
                                                    <Icon color='blue' name='mail'/>
                                                    {securityContext.security.email}
                                                </h3>
                                            </Card.Content>

                                            <Card.Content extra>
                                                <h3>
                                                    <Icon color='blue' name='pencil alternate'/>
                                                    # of Submissions = {securityContext.security.submissions}
                                                </h3>
                                            </Card.Content>

                                            <Card.Content extra>
                                                <h3>
                                                    <Icon color='blue' name='trophy'/>
                                                    Points = {securityContext.security.points}
                                                </h3>
                                            </Card.Content>

                                            <Card.Content extra>
                                                <h3>
                                                    <Icon color='blue' name='certificate'/>
                                                    { securityContext.security.is_staff ? (
                                                        'Staff'
                                                    ) : securityContext.security.is_reviewer ? (
                                                        'Reviewer'
                                                    ) : 'Newbie'
                                                    }
                                                </h3>
                                            </Card.Content>

                                            <Button.Group fluid size='big'>
                                                <Button animated='fade' negative onClick={this.cancelFunction}>
                                                    <Button.Content visible>
                                                        <Icon name='cancel' />
                                                        Cancel Changes
                                                    </Button.Content>
                                                    <Button.Content hidden>No changes will be made</Button.Content>
                                                </Button>
                                                <Button.Or />
                                                <Button animated='fade' positive onClick={this.saveFunction}>
                                                    <Button.Content visible>
                                                        <Icon name='sync' />
                                                        Save Changes
                                                    </Button.Content>
                                                    <Button.Content hidden>Changes made will be saved</Button.Content>
                                                </Button>
                                            </Button.Group>

                                            <Button
                                                animated='fade'
                                                icon
                                                basic
                                                color='red'
                                                fluid
                                                size='big'
                                                onClick={this.deleteFunction}
                                            >
                                                <Button.Content visible><Icon name='delete' />Delete Profile?</Button.Content>
                                                <Button.Content hidden>Send Request To Admin</Button.Content>
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
