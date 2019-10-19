import React, { Component, useContext } from "react";
import axios from "axios";
import validator from "validator";
import { Container, Form, Rating } from "semantic-ui-react";

import TagDropdown from "./TagDropdown";
import TagPopup from "./TagPopup";
import { SecurityContext } from "../security/SecurityContext";

export default class ResourceSubmitForm extends Component {
  static contextType = SecurityContext;

  constructor(props) {
    super(props);
    this.state = {
      url: "",
      title: "",
      rating: 1,
      tags: "",
      comments: "",
      validated: true,
      currentTags: null
    };
  }

  create_resource = () => {
    const created_by_user = this.context.security.email
      ? this.context.security.email
      : "Unknown user";

    const resource = {
      title: "Unknown title", // Backend will automatically webscrape for website title
      url: this.state.url,
      created_by_user: created_by_user,

      user_comment: this.state.comments,
      usefulness_rating: this.state.rating,
      usefulness_comment: this.state.comments,

      website_summary_metadata: "",
      website_readtime_metadata: new Date("2012.08.10"),
      website_metadata: "",
      website_title: "",

      score: 1
    };
    return resource;
  };

  post_resource = () => {
    const resource = this.create_resource();

    axios.defaults.headers = {
      "Content-Type": "application/json",
      Authorization: `Token ${this.props.token}`
    };

    axios
      .post("http://127.0.0.1:8000/api/resource/", resource)
      .then(res => {})
      .catch(error => console.error(error));
  };

  reset_resource_states = () => {
    this.setState({
      url: "",
      tags: "",
      comments: "",
      title: "refreshed",
      rating: 1,
      validated: true
    });
  };

  handleRate = (event, data) => {
    this.setState({ rating: data.rating });
  };

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = event => {
    // Validations
    if (!validator.isURL(this.state.url)) {
      this.setState({ validated: false });
      event.preventDefault();
      return;
    } else {
      this.post_resource();
      event.preventDefault();
      this.reset_resource_states();
      console.log("POST resource success");
    }
  };

  render() {
    return (
      <Container>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group>
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
          </Form.Group>

          <Form.Group>
            <Form.Input
              name="tags"
              onChange={this.handleChange}
              value={this.state.tags}
              label="Tags"
              placeholder="Enter tags separated by commas"
            />

            <Form.Input
              name="comments"
              onChange={this.handleChange}
              value={this.state.comments}
              label="Comments"
              placeholder="Enter any comments (Optional)"
            />
          </Form.Group>
          <Form.Field>
            <label>Tags</label>
            <Form.Group>
              <TagDropdown
                onChange={currentTags => this.setState({ currentTags })}
              />
              <TagPopup />
            </Form.Group>
          </Form.Field>
          <Form.Button content="Submit" />
        </Form>
      </Container>
    );
  }
}
