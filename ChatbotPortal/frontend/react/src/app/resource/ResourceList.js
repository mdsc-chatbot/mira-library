import React, { Component } from "react";
import axios from "axios";
import { List, Header, Segment, Button, Grid, Card, Container, Responsive } from "semantic-ui-react";

import ResourceListItem from "./ResourceListItem.js";
import { SecurityContext } from "../contexts/SecurityContext";
import ResourceStatistic from "./ResourceStatistic";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ResourceResponsive from "./ResourceResponsive.js";

export default class ResourceList extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resources: []
        };
    }

    get_resources = () => {
        if (this.context.security.is_logged_in) {
            // axios.defaults.headers.common = {
            //     Authorization: `Bearer ${this.context.security.token}`
            // };
            // Having the permission header loaded
            const options = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.context.security.token}`
            };
            axios
                .get("/chatbotportal/resource", {
                    params: {
                        created_by_user_pk: this.context.security.id
                    },
                    headers: options
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

        const resource_list = () => {
            return (
                <div>
                    <Container style={{ paddingBottom: 50 }} textAlign="center" vertical>
                        <ResourceStatistic resources={this.state.resources} />

                        <Link to={baseRoute + "/resource_submit"}>
                            <Button name="submit_a_resource" positive size="big">
                                Submit a resource
                            </Button>
                        </Link>
                    </Container>

                    <Card.Group itemsPerRow={3} vertical stackable>
                        {resources}
                    </Card.Group>
                </div>
            );
        };

        return <ResourceResponsive resource_component={resource_list()}></ResourceResponsive>;
    }
}
