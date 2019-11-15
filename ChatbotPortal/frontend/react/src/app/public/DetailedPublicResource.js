import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import {ResourceDetailView} from '../shared';

export default class DetailedPublicResource extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceId = this.props.resourceId;
        axios
            .get(`/api/public/retrieve/${resourceId}`)
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

DetailedPublicResource.propTypes = {
    resourceId : PropTypes.string,
};