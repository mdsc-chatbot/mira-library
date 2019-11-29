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