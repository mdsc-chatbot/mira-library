import React, { Component } from "react";
import axios from "axios";
import { List, Header, Segment, Button, Grid, Card } from "semantic-ui-react";

import ResourceListItem from "./ResourceListItem.js";
import { SecurityContext } from "../security/SecurityContext";
import ResourceStatistic from "./ResourceStatistic";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";

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
                <Segment
                    style={{ padding: "2em 0em" }}
                    textAlign="center"
                    vertical
                >
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        My Resources
                    </Header>

                    <Header as="h4" color="grey">
                        A list of all my submitted resources
                    </Header>

                    <ResourceStatistic resources={resources} />

                    <Link to={baseRoute + "/resource_submit"}>
                        <Button positive size="big">
                            Submit a resource
                        </Button>
                    </Link>
                </Segment>

                <Card.Group
                    itemsPerRow={3}
                    style={{ padding: "0em 7em" }}
                    vertical
                >
                    {resources}
                </Card.Group>
            </div>
        );
    }
}
