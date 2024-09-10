/**
 * @file: ProfilePage.js
 * @summary: Renders user's profile page and allow the user change certain user information (name, profile picture, password)
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../contexts/SecurityContext';
import {Button, Card, Container, Divider, Form, FormInput, Icon, Image, Responsive, Segment, Header} from 'semantic-ui-react';
import * as styles from "./ProfilePage.css";
import {baseRoute} from "../App";
import {Link, Redirect} from "react-router-dom";
import {object} from "prop-types";

/**
 * This class renders the profile information of a logged in user
 */
class ProfilePage extends Component {

    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {}
    }

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
                        window.location.replace(baseRoute);
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

        // Checking if an image update is required
        // If the image is selected then it should be a file object, otherwise a string of file url
        if (typeof(this.state.profile_picture) === 'object' && this.state.profile_picture !== null) {
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
                                    centered
                                />
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

                                <Header as="h3">
                                    <Icon className={styles.iconColor} name='mail'/>
                                    <Header.Content id="email"> {this.state.email} </Header.Content>
                                </Header>
                                <Divider fitted />

                                <Header as="h3">
                                    <Icon className={styles.iconColor} name='pencil alternate'/>
                                    <Header.Content id="profile_num_submissions">  # of Submissions = {this.state.submissions} </Header.Content>
                                </Header>
                                <Divider fitted />

                                {/* <Header as="h3">
                                    <Icon className={styles.iconColor} name='trophy'/>
                                    <Header.Content id="points"> Points = {this.state.points} </Header.Content>
                                </Header> */}
                                <Divider fitted />
{/* 
                                <Header as="h3">
                                    <Icon className={styles.iconColor} name='certificate'/>
                                    <Header.Content id="status"> 
                                        { this.state.is_staff ? (
                                            'Staff'
                                        ) : this.state.is_reviewer ? (
                                            'Reviewer'
                                        ) : 'Newbie'
                                        }
                                    </Header.Content>
                                </Header> */}
                                <Divider fitted/>
                                
                            </Card.Description>


                            <Button name="save" fluid size='big' animated='fade' positive onClick={event => this.handle_edit(event, this.state)}>
                                <Button.Content visible>
                                    Save Changes
                                </Button.Content>
                                <Button.Content hidden><Icon color='black' name='chevron right' /></Button.Content>
                            </Button>

                            <Link to={baseRoute + "/password"}>
                                <Button name="change_password" className={styles.changePW} color='blue' fluid size='big'>
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

                                        <Header as="h4">
                                            <Icon className={styles.iconColor} name='mail'/>
                                            <Header.Content id="email"> {this.state.email} </Header.Content>
                                        </Header>
                                        <Divider fitted />

                                        <Header as="h4">
                                            <Icon className={styles.iconColor} name='pencil alternate'/>
                                            <Header.Content id="profile_num_submissions">  # of Submissions = {this.state.submissions} </Header.Content>
                                        </Header>
                                        <Divider fitted />

                                        <Header as="h4">
                                            <Icon className={styles.iconColor} name='trophy'/>
                                            <Header.Content id="points"> Points = {this.state.points} </Header.Content>
                                        </Header>
                                        <Divider fitted />

                                        <Header as="h4">
                                            <Icon className={styles.iconColor} name='certificate'/>
                                            <Header.Content id="status"> 
                                                { this.state.is_staff ? (
                                                    'Staff'
                                                ) : this.state.is_reviewer ? (
                                                    'Reviewer'
                                                ) : 'Newbie'
                                                }
                                            </Header.Content>
                                        </Header>
                                        <Divider fitted/>

                                    </Card.Description>

                                    <Button name="save" fluid size='medium' animated='fade' positive onClick={event => this.handle_edit(event, this.state)}>
                                        <Button.Content visible>
                                            Save Changes
                                        </Button.Content>
                                        <Button.Content hidden><Icon color='black' name='chevron right' /></Button.Content>
                                    </Button>

                                <Link to={baseRoute + "/password"}>
                                    <Button className={styles.changePW} name="change_password" color='blue' fluid size='medium'>
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
