/**
 * @file: ResourceList.js
 * @summary: Component that shows list of user submitted resources, include functionality to submit a resource
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

import React, { Component } from "react";
import axios from "axios";
import { List, Header, Segment, Button, Grid, Card, Container, Responsive } from "semantic-ui-react";

import ResourceListItem from "./ResourceListItem.js";
import { SecurityContext } from "../contexts/SecurityContext";
import ResourceStatistic from "./ResourceStatistic";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ResourceResponsive from "./ResourceResponsive.js";
import ResourceSubmissionHelp from "./ResourceSubmissionHelp.js";


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

    resourcePage = () => {
        return(
            <Container style={{ paddingBottom: 50 }} textAlign="center" vertical>
                <ResourceStatistic resources={this.state.resources} />
                <Link to={baseRoute + "/resource_submit"}>
                    <Button name="submit_a_resource" color = 'green' size="medium">
                        Submit a resource
                    </Button>
                </Link>
                <ResourceSubmissionHelp trigger={
                <Button name="how_resource" color='blue' size="medium">
                        How to submit a resource?
                </Button>}/>
            </Container>
        );
    };

    render() {
        // Map resources to ResourceListItem Component
        const resources = this.state.resources.map(resource => (
            <ResourceListItem key={resource.id} resource={resource} />
        ));
        console.log(this.state.resources);

        const resource_list = () => {
            return (
                <div>
                    {this.resourcePage()}
                    <Card.Group itemsPerRow={3} vertical stackable>
                        {resources}
                    </Card.Group>
                </div>
            );
        };

        return <ResourceResponsive resource_component={resource_list()}></ResourceResponsive>;
    }
}
