import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../security/SecurityContext';
import {Button, Card, Container, Form, Icon, Image, Segment, Responsive,Divider, Grid} from 'semantic-ui-react';
import styles from "./ProfilePage.css";

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

    /*
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
            .put(this.BASE_AUTH_URL + this.context.security.id + '/update/', formData, {headers: options})
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

/* This function handles the profile page for Tablet/Computer Version */
    profilePageDataWeb = () => {
        return(<SecurityContext.Consumer>
            {(securityContext) => (
                <Form className={styles.centeredFormWeb} onSubmit={e => this.handle_edit(e, this.state)}>
                    {securityContext.security.is_logged_in ?
                        <Card fluid centered onSubmit={this.props.handle_edit}>
                            {this.state.profile_picture ? (
                                <Image src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`} size='medium' circular centered/>
                            ) : null}
                            <Form.Input className={styles.imageMobile} type='file' accept="image/png, image/jpeg" id='profile_picture' name='profile_picture' onChange={this.handleImageChange}/>
                            <Card.Content className={styles.nameMobile}>
                                <Card.Header>
                                    <Form.Group widths='equal'>

                                        <Form.Input
                                            // className={styles.fixedInputHeight}
                                            fluid
                                            label='First name'
                                            name='first_name'
                                            size='large'
                                            onChange={this.handle_change}
                                            value={this.state.first_name}
                                        />
                                        <Form.Input
                                            // className={styles.fixedInputHeight}
                                            fluid
                                            label='Last name'
                                            size='large'
                                            name='last_name'
                                            onChange={this.handle_change}
                                            value={this.state.last_name}
                                        />

                                    </Form.Group>
                                </Card.Header>
                            </Card.Content>
                            <Card.Description>
                                <Divider fitted />
                                <h3><Icon color='blue' name='mail'/>
                                    {securityContext.security.email}</h3><Divider fitted />
                                <h3>
                                    <Icon color='blue' name='pencil alternate'/>
                                    # of Submissions = {securityContext.security.submissions}
                                </h3><Divider fitted />
                                <h3>
                                    <Icon color='blue' name='trophy'/>
                                    Points = {securityContext.security.points}
                                </h3><Divider fitted />
                                <h3>
                                    <Icon color='blue' name='certificate'/>
                                    { securityContext.security.is_staff ? (
                                        'Staff'
                                    ) : securityContext.security.is_reviewer ? (
                                        'Reviewer'
                                    ) : 'Newbie'
                                    }
                                </h3><Divider fitted/>
                            </Card.Description>

                            <Button.Group fluid widths={2} size='big'>
                                <Button animated='fade' negative onClick={this.cancelFunction}>
                                    <Button.Content visible>
                                        Cancel Changes
                                    </Button.Content>
                                    <Button.Content hidden><Icon name='cancel' /></Button.Content>
                                </Button>
                                <Button.Or />
                                <Button animated='fade' positive onClick={this.saveFunction}>
                                    <Button.Content visible>
                                        Save Changes
                                    </Button.Content>
                                    <Button.Content hidden><Icon name='chevron right' /></Button.Content>
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
                </Form>
            )}
        </SecurityContext.Consumer>);
    };

    /* This function handles the profile page for Mobile Version */
    profilePageDataMobile = () => {
        return(
            <Container className={styles.segmentWeb}>
                <SecurityContext.Consumer>
                {(securityContext) => (
                    <Form className={styles.centeredFormMobile} onSubmit={e => this.handle_edit(e, this.state)}>
                        {securityContext.security.is_logged_in ?
                            <Card fluid centered onSubmit={this.props.handle_edit}>
                                {this.state.profile_picture ? (
                                    <Image src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`} centered size='medium'/>
                                ) : null}
                                <Form.Input className={styles.imageMobile} type='file' accept="image/png, image/jpeg" id='profile_picture' name='profile_picture' onChange={this.handleImageChange}/>
                                <Card.Content className={styles.nameMobile}>
                                    <Card.Header>
                                        <Form.Input
                                            fluid
                                            size = "tiny"
                                            label='First name'
                                            name='first_name'
                                            onChange={this.handle_change}
                                            value={this.state.first_name}
                                        />
                                        <Form.Input
                                            fluid
                                            size="tiny"
                                            label='Last name'
                                            name='last_name'
                                            onChange={this.handle_change}
                                            value={this.state.last_name}
                                        />
                                    </Card.Header>
                                </Card.Content>
                                <Card.Description>
                                    <Divider fitted />
                                    <h4><Icon color='blue' name='mail'/>
                                        {securityContext.security.email}</h4><Divider fitted /><h4>
                                    <Icon color='blue' name='pencil alternate'/>
                                    # of Submissions = {securityContext.security.submissions}
                                </h4><Divider fitted />
                                    <h4>
                                        <Icon color='blue' name='trophy'/>
                                        Points = {securityContext.security.points}
                                    </h4><Divider fitted />
                                    <h4>
                                        <Icon color='blue' name='certificate'/>
                                        { securityContext.security.is_staff ? (
                                            'Staff'
                                        ) : securityContext.security.is_reviewer ? (
                                            'Reviewer'
                                        ) : 'Newbie'
                                        }
                                    </h4><Divider fitted/>
                                </Card.Description>
                                <Button.Group fluid widths={2} size='small'>
                                    <Button animated='fade' negative onClick={this.cancelFunction}>
                                        <Button.Content visible>
                                            Cancel Changes
                                        </Button.Content>
                                        <Button.Content hidden><Icon name='cancel' /></Button.Content>
                                    </Button>
                                    <Button.Or />
                                    <Button animated='fade' positive onClick={this.saveFunction}>
                                        <Button.Content visible>
                                            Save Changes
                                        </Button.Content>
                                        <Button.Content hidden><Icon name='chevron right' /></Button.Content>
                                    </Button>
                                </Button.Group>
                                <Button
                                    animated='fade'
                                    icon
                                    basic
                                    color='red'
                                    fluid
                                    size='small'
                                    onClick={this.deleteFunction}
                                >
                                    <Button.Content visible><Icon name='delete' />Delete Profile?</Button.Content>
                                    <Button.Content hidden>Send Request To Admin</Button.Content>
                                </Button>
                            </Card>
                            : null}
                    </Form>
                )}
            </SecurityContext.Consumer>

            </Container>

        );
    };

    /* This function handles the responsiveness for which version to render*/
    profilePage = () => {

        return (

            <Segment.Group className={styles.segmentWeb}>

                <Responsive minWidth={768}>
                    {this.profilePageDataWeb()}
                </Responsive>

                <Responsive maxWidth={767}>
                    {this.profilePageDataMobile()}
                </Responsive>

            </Segment.Group>


        );


    };

    /**
     * This renders the ProfileForm
     * @returns {React.Fragment}
     */
    render() {
        return (
            <React.Fragment>
                <Segment.Group className={styles.segmentWeb}>
                    <Responsive maxWidth={767}>
                        {this.profilePage()}
                    </Responsive>

                    <Responsive minWidth={768}>
                        <React.Fragment>
                            <Container>
                                {this.profilePage()}
                            </Container>
                        </React.Fragment>
                    </Responsive>
                </Segment.Group>
            </React.Fragment>
        );
    }
}

export default ProfilePage;
