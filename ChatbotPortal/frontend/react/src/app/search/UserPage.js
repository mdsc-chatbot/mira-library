/**
 * @file: UserPage.js
 * @summary: Renders the user related profile information visible from the admin ends.
 *            It allows the admin to alter the user information (name, profile picture and status).
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
import {
    Button,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Container,
    Form,
    FormGroup,
    FormInput,
    Icon,
    Image,
    Label,
    Responsive,
    Segment,
    SegmentGroup
} from 'semantic-ui-react';
import * as styles from "../profile/ProfilePage.css";

class UserPage extends Component {
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
            first_name: '',
            last_name: '',
            is_active: '',
            is_reviewer: '',
            is_staff: '',
            is_editor: '',
            profile_picture: '',

            horizontal_state: ''
        };
    };

    componentDidMount() {
        this.setState({
            first_name: this.props.rowData.first_name,
            last_name: this.props.rowData.last_name,
            is_active: this.props.rowData.is_active,
            is_reviewer: this.props.rowData.is_reviewer,
            is_staff: this.props.rowData.is_staff,
            is_editor: this.props.rowData.is_editor,
            profile_picture: this.props.rowData.profile_picture
        });

        // Checking for responsiveness
        if (window.innerWidth <= 760) {
            this.setState({
                horizontal_state: false
            });
        } else {
            this.setState({
                horizontal_state: true
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
     * This function extracts the file data
     * @param event
     */
    handleImageChange = event => {
        this.setState({
            profile_picture: event.target.files[0]
        })
    };

    /**
     * This function handles the overall edit operations
     * @param e : event
     * @param editedData : data from the EditForm upon submission
     */
    handle_edit = (e, editedData) => {
        e.preventDefault();

        let formData = new FormData();
        formData.append('first_name', editedData.first_name);
        formData.append('last_name', editedData.last_name);
        formData.append('is_active', editedData.is_active);
        formData.append('is_reviewer', editedData.is_reviewer);
        formData.append('is_staff', editedData.is_staff);
        formData.append('is_editor', editedData.is_editor);

        // Checking if an image update is required
        // If the image is selected then it should be a file object, otherwise a string of file url
        if (typeof (this.state.profile_picture) === 'object') {
            formData.append('profile_picture', editedData.profile_picture);
        }

        /**
         * Perform a put request for edit.
         * Upon successful response, set the security context and component props with response data.
         * Otherwise, send an error is thrown."
         */
        axios
            .put(`/chatbotportal/authentication/super/${this.props.rowData.id}/update/`, formData,
                {headers: {'Authorization': `Bearer ${this.context.security.token}`}})
            .then(
                response => {
                    console.log(response.data)
                    this.setState(response.data);
                    window.location.reload();

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
        if (this.context.security.id!= this.props.rowData.id){
            axios
                .delete(`/chatbotportal/authentication/delete/${this.props.rowData.id}/`, {headers: options})
                .then(
                    response => {
                        console.log(response.status)
                        window.location.reload();

                    },
                    error => {
                        console.log(error);
                    }
                );

        }
    } 
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

    set_mobile_format = () => {
        if (window.innerWidth <= 760) {
            this.setState({
                horizontal_state: false
            });
        } else {
            this.setState({
                horizontal_state: true
            });
        }
    };

    /**
     * This renders the ProfileForm
     * @returns {React.Fragment}
     */
    render() {
        return (
            <React.Fragment>
                <Responsive as={Container} minWidth={320} onUpdate={this.set_mobile_format}>
                    <Container>
                        <Form>
                            <Segment>
                                <Label
                                    size='big'
                                    as='h1'
                                    icon='user'
                                    color='red'
                                    content={this.state.first_name ? `${this.state.first_name}'s Profile` : `${this.state.id}'s profile`}
                                    ribbon>
                                </Label>
                                <Card fluid
                                      centered>
                                    {typeof (this.state.profile_picture) !== 'object' && this.state.profile_picture ? (
                                        <Image
                                            src={`/static/${this.state.profile_picture.split('/')[this.state.profile_picture.split('/').length - 1]}`}
                                            size='medium'
                                            circular
                                            centered/>
                                    ) : null}
                                    <FormInput
                                        className={styles.imageMobile}
                                        type='file'
                                        accept="image/png, image/jpeg"
                                        id='profile_picture'
                                        name='profile_picture'
                                        onChange={this.handleImageChange}/>
                                    <CardContent>
                                        <CardHeader>
                                            <FormGroup widths='equal' unstackable>
                                                <FormInput
                                                    className={styles.fixedInputHeight}
                                                    fluid
                                                    // label='First name'
                                                    name='first_name'
                                                    onChange={this.handle_change}
                                                    placeholder="First Name"
                                                    value={this.state.first_name}/>
                                                <FormInput
                                                    className={styles.fixedInputHeight}
                                                    fluid
                                                    // label='Last name'
                                                    name='last_name'
                                                    onChange={this.handle_change}
                                                    placeholder="Last Name"
                                                    value={this.state.last_name}/>
                                            </FormGroup>
                                        </CardHeader>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='id badge'/>
                                            {this.props.rowData.id}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='mail'/>
                                            {this.props.rowData.email}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='dropbox'/>
                                            Submissions: {this.props.rowData.submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='thumbs up'/>
                                            Reviewed: {this.props.rowData.approved_submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='wait'/>
                                            Pending: {this.props.rowData.pending_submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='trophy'/>
                                            Points: {this.props.rowData.points}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3><Icon color='red' name='heart'/>
                                            Affiliation: </h3> {this.props.rowData.affiliation}
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='sign in'/>
                                            Last logged: {this.props.rowData.last_login}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='registered'/>
                                            Registered on: {this.props.rowData.date_joined}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <SegmentGroup horizontal={this.state.horizontal_state}>
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
                                            <Segment color='red'>
                                                <Checkbox
                                                    checked={this.state.is_editor}
                                                    label='Editor'
                                                    name='is_editor'
                                                    value={this.state.is_editor}
                                                    onChange={this.handle_toggle}
                                                    slider
                                                />
                                            </Segment>
                                        </SegmentGroup>

                                        <SegmentGroup horizontal={this.state.horizontal_state} size={"mini"}>
                                            <Segment>
                                                <Button
                                                    color='green'
                                                    fluid
                                                    size='small'
                                                    onClick={e => this.handle_edit(e, this.state)}>
                                                    <Icon name='save'/>Save
                                                </Button>
                                            </Segment>
                                            <Segment>
                                                <Button
                                                    color='red'
                                                    fluid
                                                    size='small'
                                                    onClick={e => this.handle_delete(e)}>
                                                    <Icon name='delete'/>Delete
                                                </Button>
                                            </Segment>
                                        </SegmentGroup>
                                    </CardContent>
                                </Card>
                            </Segment>
                        </Form>
                    </Container>
                </Responsive>
            </React.Fragment>
        );
    }
}

export default UserPage;
