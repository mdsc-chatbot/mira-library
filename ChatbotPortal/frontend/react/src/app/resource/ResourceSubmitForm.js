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
      title: "Unknown title",
      url: "",
      rating: 1,
      comments: "",

      tags: [],
      validated: true,
      currentTags: null
    };
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

    axios
      .post("http://127.0.0.1:8000/api/resource/", resource)
      .then(res => {})
      .catch(error => console.error(error));
  };

  reset_resource_states = () => {
    this.setState({
      title: "Unknown title",
      url: "",
      rating: 1,
      comments: "",

      tags: [],
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
    if (!validator.isURL(this.state.url) || !this.state.rating) {
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
            <Form.Field>
              <label>Tags</label>
              <Form.Group>
                <TagDropdown value={this.state.tags} onChange={tags => this.setState({ tags })} />
                <TagPopup />
              </Form.Group>
            </Form.Field>
            <Form.Input
              name="comments"
              onChange={this.handleChange}
              value={this.state.comments}
              label="Comments"
              placeholder="Enter any comments (Optional)"
            />
          </Form.Group>

          <Form.Button content="Submit" />
        </Form>
      </Container>
    );
  }
}
