import React, { Component } from "react";
import axios from "axios";
import { ResourceDetailView } from "../shared";
import { SecurityContext } from "../security/SecurityContext";

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
            <div>
                <Responsive as={Segment} {...Responsive.onlyMobile}>
                    <div style={{ paddingTop: 30, paddingLeft: 15, paddingRight: 15, paddingBottom: 30 }}>
                        <ResourceDetailView resource={this.state.resource} />
                    </div>
                </Responsive>
                <Responsive as={Segment} minWidth={768}>
                    <div style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30 }}>
                        <ResourceDetailView resource={this.state.resource} />
                    </div>
                </Responsive>
            </div>
        );
    }
}
