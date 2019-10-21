import React, { Component } from "react";
import { List, Rating } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { baseRoute } from "../App";

export default class ResourceListItem extends Component {
  render() {
    const resource = this.props.resource;

    return (
      <List.Item>
        <List.Icon name="globe" size="large" verticalAlign="middle" />
        <List.Content>
          <List.Header>
            <Link to={baseRoute + "/resource/" + resource.id}>
              {resource.title}
            </Link>
          </List.Header>
          <Rating
            icon="star"
            defaultRating={resource.rating}
            maxRating={5}
            disabled
          />
        </List.Content>
      </List.Item>
    );
  }
}
