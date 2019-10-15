import React, { Component } from "react";
import { Container, Form, Rating, Button } from "semantic-ui-react";
import axios from "axios";

export default class ResourceSubmitForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "",
      title: "",
      rating: "",
      tags: "",
      comments: ""
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

  handleSubmit(event) {
    console.log("clicked");
    const created_resource = {
      title: "Unknown",
      url: this.state.url,

      user_comment: this.state.comments,
      usefulness_rating: this.state.rating,
      usefulness_comment: this.state.comments,

      website_summary_metadata: "models.TextField()",
      website_readtime_metadata: "models.DateTimeField()",
      website_metadata: "models.TextField()",
      website_title: "models.TextField()",

      score: 1
    };

    console.log(created_resource);
    axios
      .post(
        "http://127.0.0.1:8000/api/user/resources/create/",
        created_resource
      )
      .then(res => {})
      .catch(error => console.error(error));

    console.log("axios");
    event.preventDefault();
  }

  render() {
    return (
      <Container>
        <Form>
          <Form.Group>
            <Form.Field name="url" onChange={this.handleChange}>
              <label>Enter URL</label>
              <input placeholder="xxx@yyy.ca" />
            </Form.Field>
            <Form.Field name="rating" onChange={this.handleChange}>
              <label>Rating</label>
              <Rating
                maxRating={5}
                defaultRating={3}
                icon="star"
                size="massive"
              />
            </Form.Field>
          </Form.Group>
          <Form.Group>
            <Form.Field name="tags" onChange={this.handleChange}>
              <label>Tags</label>
              <input placeholder="Enter tags separated by commas" />
            </Form.Field>
            <Form.Field name="comments" onChange={this.handleChange}>
              <label>Comments</label>
              <input placeholder="Enter any comments (Optional)" />
            </Form.Field>
          </Form.Group>
          <Button type="submit" onClick={this.handleSubmit}>
            Submit
          </Button>
        </Form>
      </Container>
    );
  }
}
