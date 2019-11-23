import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../contexts/SecurityContext';
import {Button, Card, Container, Divider, Form, FormInput, Icon, Image, Responsive, Segment} from 'semantic-ui-react';
import styles from "./ProfilePage.css";
import {baseRoute} from "../App";
import {Link, Redirect} from "react-router-dom";

/**
 * This class renders the profile information of a logged in user
 */
class ProfilePage extends Component {

    static contextType = SecurityContext;

    componentDidMount() {
        this.retrieve_user_info();
    }

    /**
     * Get the current logged in user's information
     */
    retrieve_user_info = () => {
        axios
            .get('/chatbotportal/authentication/currentuser/', {withCredentials: true})
            .then(
                response => {
                    /**
                     * If the response data is not empty set is_logged_in status to true, otherwise false
                     */
                    if (response.data !== '') {
                        response.data['is_logged_in'] = true;
                        this.setState(response.data);
                    } else {
                        response.data = JSON.parse('{}');
                        response.data['is_logged_in'] = false;
                        this.setState(response.data);
                    }
                },
                error => {
                    console.log(error);
                }
            );
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
     * This function extracts the file data
     * @param event
     */
    handleImageChange = event => {
        this.setState({
            profile_picture: event.target.files[0]
        })
    };

    /*
     * This function handles the overall edit operations
     * @param e : event
     * @param editedData : data from the EditForm upon submission
     */
    handle_edit = (event, editedData) => {
        event.preventDefault();

        let formData = new FormData();
        formData.append('first_name', editedData.first_name);
        formData.append('last_name', editedData.last_name);
        if (this.state.profile_picture) {
            formData.append('profile_picture', editedData.profile_picture);
        }

        /**
         * Perform a put request for edit.
         * Upon successful response, set the security context and component props with response data.
         * Otherwise, send an error is thrown."
         */
        axios
            .put(
                `/chatbotportal/authentication/${this.context.security.id}/update/`,
                formData,
                {headers: {'Authorization': `Bearer ${this.context.security.token}`}})
            .then(
                response => {
                    console.log(response.data);
                    this.setState(response.data);
                    this.context.setSecurity(response.data);
                    // Reloading the page after modal closes
                    window.location.reload();
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
                <Form className={styles.centeredFormWeb}>
                    {securityContext.security.is_logged_in ?
                        <Card fluid centered>
                            {typeof(this.state.profile_picture) !== 'object' && this.state.profile_picture? (
                                <Image
                                    src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`}
                                    size='medium'
                                    circular
                                    centered/>
                            ) : null}
                            <Form.Input
                                className={styles.imageMobile}
                                type='file'
                                accept="image/png, image/jpeg"
                                id='profile_picture'
                                name='profile_picture'
                                onChange={this.handleImageChange}/>
                            <Card.Content className={styles.nameMobile}>
                                <Card.Header>
                                    <Form.Group widths='equal'>
                                        <Form.Input
                                            fluid
                                            label='First name'
                                            name='first_name'
                                            size='large'
                                            onChange={this.handle_change}
                                            value={this.state.first_name}
                                        />
                                        <Form.Input
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


                            <Button fluid size='big' animated='fade' positive onClick={event => this.handle_edit(event, this.state)}>
                                <Button.Content visible>
                                    Save Changes
                                </Button.Content>
                                <Button.Content hidden><Icon name='chevron right' /></Button.Content>
                            </Button>

                            <Link to={baseRoute + "/password"}>
                                <Button color='blue' fluid size='big'>
                                    Change Password
                                </Button>
                            </Link>
                        </Card>
                        : null}
                </Form>
            )}
        </SecurityContext.Consumer>);
    };

    /* This function handles the profile page for Mobile Version */
    profilePageDataMobile = () => {
        return(
                <SecurityContext.Consumer>
                    {(securityContext) => (
                        <Form className={styles.centeredFormMobile}>
                            {securityContext.security.is_logged_in ?
                                <Card fluid centered>
                                    {typeof(this.state.profile_picture) !== 'object' && this.state.profile_picture? (
                                        <Image
                                            src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`}
                                            centered
                                            size='small'/>
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

                                    <Button fluid size='medium' animated='fade' positive onClick={event => this.handle_edit(event, this.state)}>
                                        <Button.Content visible>
                                            Save Changes
                                        </Button.Content>
                                        <Button.Content hidden><Icon name='chevron right' /></Button.Content>
                                    </Button>

                                    <Link to={baseRoute + "/password"}>
                                        <Button color='blue' fluid size='medium'>
                                            Change Password
                                        </Button>
                                    </Link>
                                </Card>
                                : null}
                        </Form>
                    )}
                </SecurityContext.Consumer>
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
                        {this.profilePageDataMobile()}
                    </Responsive>

                    <Responsive minWidth={768}>
                        <React.Fragment>
                            <Container>
                                {this.profilePageDataWeb()}
                            </Container>
                        </React.Fragment>
                    </Responsive>
                </Segment.Group>
            </React.Fragment>
        );
    }
}

export default ProfilePage;
