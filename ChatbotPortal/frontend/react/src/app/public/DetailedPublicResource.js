import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import {ResourceDetailView} from '../shared';
import {SecurityContext} from '../contexts/SecurityContext';

export default class DetailedPublicResource extends React.Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceId = this.props.resourceId;
        const retrieve_url = this.context.security.is_reviewer || this.context.security.is_superuser ? 'retrieve-admin' : 'retrieve';

        axios
            .get(`/api/public/${retrieve_url}/${resourceId}`, {
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
            <ResourceResponsive resource_component={<ResourceDetailView resource={this.state.resource}/>}/>
        );
    }
}

DetailedPublicResource.propTypes = {
    resourceId : PropTypes.string,
};