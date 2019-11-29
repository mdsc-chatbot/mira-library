/**
 * @file: ResourceDetail.js
 * @summary: Component that shows resource detail on user side
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
import { ResourceDetailView } from "../shared";
import { SecurityContext } from "../contexts/SecurityContext";
import ResourceResponsive from "./ResourceResponsive";

export default class ResourceDetail extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {},
            tags:{},
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
                console.log(res.data)
            });
        axios
            .get(`/chatbotportal/resource/get-tags/${resourceID}`, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(res => {
                this.setState({
                    tags: res.data
                });
                console.log(res.data)
            });
    }

    render() {
        const viewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";
        return (
            <ResourceResponsive
                resource_component={<ResourceDetailView resource={this.state.resource} tagsGot={this.state.tags} viewer={viewer}/>}
            ></ResourceResponsive>
        );
    }
}
