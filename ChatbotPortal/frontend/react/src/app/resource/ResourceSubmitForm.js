import React, { Component, useContext } from "react";
import axios from "axios";
import validator from "validator";
import {
    Container,
    Form,
    Rating,
    Segment,
    Header,
    Message,
    Input
} from "semantic-ui-react";

import TagDropdown from "./TagDropdown";
import { SecurityContext } from "../security/SecurityContext";
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

            tags: [],
            validated: true,
            currentTags: null,
            submitted: 0
        };
        this.baseState = this.state;
    }

    create_resource = () => {
        // Get current logged in user
        const created_by_user = this.context.security.is_logged_in
            ? this.context.security.email
            : "Unknown user";

        const resourceFormData = new FormData();

        resourceFormData.append("title", "Unknown title");
        resourceFormData.append("url", this.state.url);
        resourceFormData.append("rating", this.state.rating);
        resourceFormData.append("comments", this.state.comments);
        resourceFormData.append("created_by_user", created_by_user);
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
        axios.defaults.headers.common = {
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .post("http://127.0.0.1:8000/api/resource/", resourceFormData)
            .then(res => {})
            .catch(error => {
                console.error(error);
                return -1;
            });

        return 1;
    };

    handleRate = (event, data) => {
        this.setState({ rating: data.rating });
    };

    handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
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
        if (!validator.isURL(this.state.url) || !this.state.rating) {
            this.setState({ validated: false });
            event.preventDefault();
            return;
        } else {
            this.setState({ submitted: this.post_resource() }, () => {
                setTimeout(() => {
                    this.setState(this.baseState);
                }, 1000);
            });
            event.preventDefault();
            console.log("POST resource success");
        }
    };

    render() {
        return (
            <div
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30, }}
            >
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
                        {this.state.validated ? (
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
                                    content: "Please enter a url",
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
                            <label>Tags</label>
                            <Form.Group className={styles.dropdownPadding}>
                                <TagDropdown
                                    value={this.state.tags}
                                    onChange={tags => this.setState({ tags })}
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
                                            content="You've submitted a resource!"
                                        />
                                    );
                                else if (this.state.submitted === -1)
                                    return (
                                        <Message
                                            error
                                            header="Submit failure"
                                            content="Your submission of a resource is not accepted."
                                        />
                                    );
                                else return <div></div>;
                            })()}
                        </div>

                        <Form.Button name="submit" content="Submit" color="green" />
                    </Form>
                </Container>
            </div>
        );
    }
}
