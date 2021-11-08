/**
 * @file: DetailPublicResource.js
 * @summary: Componenent that renders detail view of a public resource
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
import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import {ResourceDetailView} from '../shared';
import {resourceReview} from '../shared';
import {SecurityContext} from '../contexts/SecurityContext';
import ResourceResponsive from '../resource/ResourceResponsive';

export default class DetailedPublicResource extends React.Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {},
            tags:{},
            reviews:{},
        };
    }

    componentDidMount() {
        const resourceId = this.props.resourceId;
        const retrieve_url = this.context.security.is_reviewer || this.context.security.is_superuser ? 'retrieve-admin' : 'retrieve';
        const headers = {};
        if (this.context.security.token) {
            headers['Authorization'] = `Bearer ${this.context.security.token}`;
        }

        axios
            .get(`/api/public/${retrieve_url}/${resourceId}`, {
                headers
            })
            .then(res => {
                res.data.comments = ""
                this.setState({
                    resource: res.data
                });
            });
        axios
            .get(`/chatbotportal/resource/get-tags/${resourceId}`, {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(res => {
                this.setState({
                    tags: res.data
                });
            });
    }

    render() {
        return (
        <ResourceResponsive resource_component={<ResourceDetailView resource={this.state.resource} tagsGot={this.state.tags} viewer='' />}/>
        );
    }
}

DetailedPublicResource.propTypes = {
    resourceId : PropTypes.string,
};