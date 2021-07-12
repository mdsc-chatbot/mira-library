/**
 * @file: ResourceSubmitForm.js
 * @summary: Component that allows user to inputs information to submit a resource (handle validations)
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

import React, {Component} from "react";
import axios from "axios";
import validator from "validator";
import {Container, Form, Header, Input, Message, Rating, Icon} from "semantic-ui-react";

import TagDropdown from "./TagDropdown";
import CategoryDropdown from './CategoryDropdown';
import {SecurityContext} from '../contexts/SecurityContext';
import styles from "./ResourceSubmitForm.css";
import ResourceSubmissionHelp from "./ResourceSubmissionHelp.js"

export default class ResourceSubmitForm extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            title: "",
            url: "",
            rating: 1,
            attachment: null,
            attachmentPath: "", // To clear the file after submitting it
            comments: "",
            definition: "",
            email: "",
            phone_number: "",

            category: 1,
            tags: [],
            url_validated: true,
            currentTags: null,
            submitted: 0
        };
        this.baseState = this.state;
    }

    create_resource = () => {
        // Get current logged in user
        let created_by_user = null;
        let created_by_user_pk = null;
        if (this.context.security.is_logged_in) {
            created_by_user = this.context.security.first_name;
            created_by_user_pk = this.context.security.id;
        }
        const resourceFormData = new FormData();

        resourceFormData.append("title", this.state.title);
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("created_by_user", created_by_user);
        resourceFormData.append("created_by_user_pk", created_by_user_pk);
        resourceFormData.append("category", this.state.category);
        resourceFormData.append("email", this.state.email);
        resourceFormData.append("definition", this.state.definition);
        resourceFormData.append("phone_number", this.state.phone_number);
        this.state.attachment !== null
            ? resourceFormData.append("attachment", this.state.attachment)
            : null;

        // Submission for tags
        // Lists have to be submitted in a certain way in order for the server to recognize it
        if (this.state.tags && this.state.tags.length) {
            this.state.tags.forEach(value => {
                resourceFormData.append(`tags`, value);
            });
        }

        return resourceFormData;
    };

    post_resource = () => {
        const resourceFormData = this.create_resource();
        // let submitted = 1;

        axios
            .post("/chatbotportal/resource/", resourceFormData, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(() => {
                this.set_submitted_state(1, "POST SUCESS");
            })
            .catch(error => {
                console.error(error);
                this.set_submitted_state(-1, "POST FAILURE");
            });

    };

    set_submitted_state = (submitted_value, submitted_message) => {
        console.log(this.state, submitted_value)
        if (submitted_value === 1) {
            this.update_user_submissions();
        }
        this.setState({submitted: submitted_value}, () => {
            setTimeout(() => {
                this.setState(this.baseState);
            }, 1000);
        });
        console.log(submitted_message);
    };

    update_user_submissions = () => {
        axios
            .put(`/chatbotportal/authentication/${this.context.security.id}/update/submissions/`, '', {
                headers: { 'Authorization': `Bearer ${this.context.security.token}` }
            })
            .then(
                () => {},
                error => {
                    console.log(error);
                }
            );
    };

    handleRate = (event, data) => {
        this.setState({rating: data.rating});
    };

    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
    };

    // event.target.value holds the pathname of a file
    handleFileChange = event => {
        this.setState({
            [event.nativeEvent.target.name]: event.nativeEvent.target.files[0],
            attachmentPath: event.nativeEvent.target.value
        });
    };

    handleSubmit = event => {
        // Validations
        if (!validator.isURL(this.state.url) || !this.state.url) {
            this.setState({url_validated: false});
        } else {
            this.post_resource();
        }
        event.preventDefault();
    };

    render() {
        return (
            <div style={{ paddingTop: "3%", paddingLeft: "10%", paddingRight: "10%", paddingBottom: "3%" }}>
                <SecurityContext.Consumer>
                    {securityContext => (
                        <Container vertical>
                            <Header
                                as="h3"
                                style={{
                                    fontSize: "2em"
                                }}
                                color="blue"
                            >
                                Resource submission
                            </Header>
                            <Form onSubmit={this.handleSubmit} success error>
                                <ResourceSubmissionHelp style={{display:'inline-block'}} trigger={
                                    <Icon name='question circle'/>
                                }/>
                                {securityContext.security.is_logged_in ? (
                                    <div>
                                        <Form.Input
                                                fluid
                                                required
                                                name="title"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.title}
                                                label="Enter Title"
                                                placeholder="title"
                                            />
                                            <Form.Input
                                                fluid
                                                name="phone_number"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.phone_number}
                                                label="Enter Phone Number"
                                                placeholder="###########"
                                            />
                                            <Form.Input
                                                fluid
                                                name="email"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.email}
                                                label="Enter Email Address"
                                                placeholder="Email"
                                            />
                                        {this.state.url_validated ? (
                                            <Form.Input
                                                name="url"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.url}
                                                label="Enter URL"
                                                placeholder="https://"
                                            />
                                        ) : (
                                            <Form.Input
                                                error={{
                                                    content: "Please enter a valid url",
                                                    pointing: "below"
                                                }}
                                                fluid
                                                required
                                                name="url"
                                                onChange={this.handleChange}
                                                width={16}
                                                value={this.state.url}
                                                label="Enter URL"
                                                placeholder="https://"
                                            />
                                        )}

                                        <Form.Field>
                                            <label>Resource Usefulness Rating</label>
                                            <Rating
                                                name="rating"
                                                onRate={this.handleRate}
                                                onChange={this.handleChange}
                                                value={this.state.rating}
                                                label="Rating"
                                                defaultRating={this.state.rating}
                                                maxRating={5}
                                                icon="star"
                                                size="massive"
                                            />
                                        </Form.Field>
                                        
                                        <Form.Field>
                                            <label>Category</label>
                                            <CategoryDropdown
                                                value={this.state.category}
                                                onChange={category => this.setState({ category })}
                                            />
                                        </Form.Field>

                                        <Form.Field>
                                            <label>Age Tags</label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Age Group"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Location Tags</label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Locations"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Health Issue Tags</label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Health Issue Group"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Language Tags</label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    tagCat="Language"
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>
                                        <Form.Field>
                                            <label>Misc Tags</label>
                                            <Form.Group className={styles.dropdownPadding}>
                                                <TagDropdown
                                                    name="tags"
                                                    value={this.state.tags}
                                                    onChange={tags => this.setState({ tags })}
                                                />
                                            </Form.Group>
                                        </Form.Field>

                                        <Form.TextArea
                                            name="definition"
                                            onChange={this.handleChange}
                                            value={this.state.definition}
                                            label="Definition"
                                            placeholder="Enter a definition, if applicable."
                                        />

                                        <Form.TextArea
                                            name="comments"
                                            onChange={this.handleChange}
                                            value={this.state.comments}
                                            label="Comments"
                                            placeholder="Enter any comments (Optional)"
                                        />

                                        <Form.Field>
                                            <label>Upload an attachment</label>
                                            <Input
                                                type="file"
                                                name="attachment"
                                                value={this.state.attachmentPath}
                                                onChange={this.handleFileChange}
                                            />
                                        </Form.Field>

                                        <div>
                                            {(() => {
                                                if (this.state.submitted === 1)
                                                    return (
                                                        <Message success header="Submit success">
                                                            <Message.Content name="submit_success">
                                                                Congratulations! You've submitted a
                                                                resource!
                                                            </Message.Content>
                                                        </Message>
                                                    );
                                                else if (this.state.submitted === -1)
                                                    return (
                                                        <Message
                                                            error header="Submit failure">
                                                            <Message.Content name="submit_failure">
                                                                Something went wrong! Your resource
                                                                is not submitted.
                                                            </Message.Content>
                                                        </Message>
                                                    );
                                                else return <div />;
                                            })()}
                                        </div>

                                        <Form.Button name="submit" content="Submit" color="green" />
                                    </div>
                                ) : null}
                            </Form>
                        </Container>
                    )}
                </SecurityContext.Consumer>
            </div>
        );
    }
}
