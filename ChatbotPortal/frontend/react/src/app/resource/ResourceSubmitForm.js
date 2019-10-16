import React, { Component } from "react";
import { Container, Form, Rating, Button } from "semantic-ui-react";
import axios from "axios";
import validator from "validator";

export default class ResourceSubmitForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      title: "",
      rating: 1,
      tags: "",
      comments: "",
      validated: true
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    let name = event.target.name;
    let value = event.target.value;
    this.setState({ [name]: value });
    console.log(name, value);
  }

  handleRate = (event, data) => {
    this.setState({ rating: data.rating });
  };

  handleSubmit(event) {
    console.log("clicked");

    // Validations
    if (!validator.isURL(this.state.url)) {
      this.setState({ validated: false });
      event.preventDefault();
      return;
    }

    const created_resource = {
      title: "New resources",
      url: this.state.url,
      created_by_user: "user",

      user_comment: this.state.comments,
      usefulness_rating: this.state.rating,
      usefulness_comment: this.state.comments,

      website_summary_metadata: "models.TextField()",
      website_readtime_metadata: new Date("2012.08.10"),
      website_metadata: "models.TextField()",
      website_title: "models.TextField()",

      score: 1
    };

    console.log(created_resource);

    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.headers = {
      "Content-Type": "application/json",
      Authorization: `Token ${this.props.token}`
    };

    axios
      .post("http://127.0.0.1:8000/api/user/resources/", created_resource)
      .then(res => {})
      .catch(error => console.error(error));

    console.log("axios");

    event.preventDefault();
    this.setState({
      url: "",
      tags: "",
      comments: "",
      title: "refreshed",
      rating: 1,
      validated: true
    });
  }

  render() {
    return (
      <Container>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group>
            {this.state.validated ? (
              <Form.Input
                label="Enter URL"
                placeholder="https://"
                required
                name="url"
                onChange={this.handleChange}
                width={6}
                value={this.state.url}
              />
            ) : (
              <Form.Input
                error={{
                  content: "Please enter a url",
                  pointing: "below"
                }}
                fluid
                label="Enter URL"
                placeholder="https://"
                required
                name="url"
                onChange={this.handleChange}
                width={6}
                value={this.state.url}
              />
            )}
            <Rating
              label="Rating"
              maxRating={5}
              defaultRating={this.state.rating}
              icon="star"
              size="massive"
              onRate={this.handleRate}
              onChange={this.handleChange}
              value={this.state.rating}
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
          <Form.Button content="Submit" />
        </Form>
      </Container>
    );
  }
}
