import React, { Component } from "react";
import axios from "axios";
import { List } from "semantic-ui-react";

import ResourceListItem from "./ResourceListItem.js";

export default class ResourceList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      resources: []
    };
  }

  fetchResources = () => {
    axios.get("http://127.0.0.1:8000/api/resource").then(res => {
      this.setState({
        resources: res.data
      });
    });
  };

  componentDidMount() {
    this.fetchResources();
  }

  componentWillReceiveProps(newProps) {
    if (newProps.token) {
      this.fetchResources();
    }
  }

  render() {
    const resources = this.state.resources.map(resource => (
      <ResourceListItem key={resource.id} resource={resource} />
    ));

    return (
      <div>
        <List selection verticalAlign="middle">
          {resources}
        </List>
      </div>
    );
  }
}
