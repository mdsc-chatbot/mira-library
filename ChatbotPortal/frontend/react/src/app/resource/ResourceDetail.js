import React, { Component } from "react";
import axios from "axios";
import {ResourceDetailView} from '../shared';

export default class ResourceDetail extends Component {
    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceID = this.props.match.params.resourceID;
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}`)
            .then(res => {
                this.setState({
                    resource: res.data
                });
            });
    }

    render() {
        return (
            <ResourceDetailView resource={this.state.resource} />
        );
    }
}
