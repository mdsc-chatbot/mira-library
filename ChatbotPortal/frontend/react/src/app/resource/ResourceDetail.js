import React, { Component } from "react";
import axios from "axios";
import {ResourceDetailView} from '../shared';
import { SecurityContext } from "../contexts/SecurityContext";
import ResourceResponsive from "./ResourceResponsive";

export default class ResourceDetail extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceID = this.props.match.params.resourceID;
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}`, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(res => {
                this.setState({
                    resource: res.data
                });
            });
    }

    render() {
        return (
            <ResourceResponsive
                resource_component={<ResourceDetailView resource={this.state.resource} />}
            ></ResourceResponsive>
        );
    }
}
