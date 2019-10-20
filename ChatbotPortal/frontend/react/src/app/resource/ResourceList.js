import React, { Component } from "react";
import axios from "axios";
import { List, Header } from "semantic-ui-react";

import ResourceListItem from "./ResourceListItem.js";
import { SecurityContext } from "../security/SecurityContext";
import Statistics from "./Statistics";

export default class ResourceList extends Component {
  static contextType = SecurityContext;

  constructor(props) {
    super(props);

    this.state = {
      resources: []
    };
  }

  get_resources = () => {
    if (this.context.security.email) {
      axios
        .get("http://127.0.0.1:8000/api/resource", {
          params: {
            created_by_user: this.context.security.email
          }
        })
        .then(res => {
          this.setState({
            resources: res.data
          });
        });
    }
  };

  componentDidMount() {
    this.get_resources();
  }

  componentWillReceiveProps(newProps) {
    if (newProps.token) {
      this.get_resources();
    }
  }

  render() {
    // Map resources to ResourceListItem Component
    const resources = this.state.resources.map(resource => (
      <ResourceListItem key={resource.id} resource={resource} />
    ));
    console.log(this.state.resources);

    return (
      <div>
        <Header as="h2">Resources</Header>
        <Statistics resources={resources} />
        <List selection verticalAlign="middle" className="centered">
          {resources}
        </List>
      </div>
    );
  }
}
