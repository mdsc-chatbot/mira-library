import React, {Component} from "react";
import axios from "axios";
import validator from "validator";
import {Container, Form, Header, Input, Message, Rating} from "semantic-ui-react";

import TagDropdown from "./TagDropdown";
import CategoryDropdown from './CategoryDropdown';
import {SecurityContext} from '../security/SecurityContext';
import styles from "./ResourceSubmitForm.css";

export default class ResourceSubmitForm extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            title: "Unknown title",
            url: "",
            rating: 1,
            attachment: null,
            attachmentPath: "", // To clear the file after submitting it
            comments: "",

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

        resourceFormData.append("title", "Unknown title");
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("created_by_user", created_by_user);
        resourceFormData.append("created_by_user_pk", created_by_user_pk);
        resourceFormData.append("category", this.state.category);
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

        axios.defaults.headers.common = {
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .post("/chatbotportal/resource/", resourceFormData)
            .then(() => {
            })
            .catch(error => {
                console.error(error);
                this.set_submitted_state(-1, "POST FAILURE");
            });

        this.set_submitted_state(1, "POST SUCESS");
    };

    set_submitted_state = (submitted_value, submitted_message) => {
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
        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };
        axios
            .put(
                `/chatbotportal/authentication/${this.context.security.id}/update/submissions/`, {headers: options})
            .then(
                () => {
                },
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
            <div style={{paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30}}>
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
                    <SecurityContext.Consumer>
                        {(securityContext) => (

                            <Form onSubmit={this.handleSubmit} success error>
                                {securityContext.security.is_logged_in ? <div>
                                    {this.state.url_validated ? (
                                        <Form.Input
                                            required
                                            name="url"
                                            onChange={this.handleChange}
                                            width={6}
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
                                            width={6}
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
                                        <label>Tags</label>
                                        <Form.Group className={styles.dropdownPadding}>
                                            <TagDropdown
                                                value={this.state.tags}
                                                onChange={tags => this.setState({tags})}
                                            />
                                        </Form.Group>
                                    </Form.Field>
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
                                                    <Message
                                                        success
                                                        header="Submit success"
                                                        content="Congratulations! You've submitted a resource!"
                                                    />
                                                );
                                            else if (this.state.submitted === -1)
                                                return (
                                                    <Message
                                                        error
                                                        header="Submit failure"
                                                        content="Something went wrong! Your resource is not submitted."
                                                    />
                                                );
                                            else return <div/>;
                                        })()}
                                    </div>

                                    <Form.Button name="submit" content="Submit" color="green"/></div> : null}
                            </Form>
                        )}
                    </SecurityContext.Consumer>
                </Container>
            </div>
        );
    }
}
