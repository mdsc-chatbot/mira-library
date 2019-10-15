import React, { Component } from "react";
import { List, Rating } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { baseRoute } from "../App";

export default class ResourceListItem extends Component {
  render() {
    const resource = this.props.resource;
    const resource_link = baseRoute + "/resource/" + resource.id;
    console.log(resource.usefulness_rating, typeof resource.usefulness_rating);

    return (
      <List.Item>
        <List.Icon name="globe" size="large" verticalAlign="middle" />
        <List.Content>
          <List.Header>
            <Link to={resource_link}>{resource.title}</Link>
          </List.Header>
          <Rating
            icon="star"
            defaultRating={resource.usefulness_rating}
            maxRating={5}
            disabled
          />
        </List.Content>
      </List.Item>
    );
  }
}
