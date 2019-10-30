import React, { Component, useContext } from "react";
import axios from "axios";
import validator from "validator";
import {
    Container,
    Form,
    Rating,
    Segment,
    Header,
    Message
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
        const created_by_user = this.context.security.email
            ? this.context.security.email
            : "Unknown user";

        const resource = {
            title: "Unknown title", // Backend will automatically webscrape for website title
            url: this.state.url,
            rating: this.state.rating,
            tags: this.state.tags,
            comments: this.state.comments,
            created_by_user: created_by_user
        };
        return resource;
    };

    post_resource = () => {
        const resource = this.create_resource();
        axios.defaults.headers.common = {
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .post("http://127.0.0.1:8000/api/resource/", resource)
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
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100 }}
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
                            <label>Resource Quality</label>
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

                        <Form.Button content="Submit" color="green" />
                    </Form>
                </Container>
            </div>
        );
    }
}
