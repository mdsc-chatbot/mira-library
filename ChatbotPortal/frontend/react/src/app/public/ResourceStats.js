import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import {ResourceStatGroup} from '../public/ResourceStatGroup';
import {SecurityContext} from '../contexts/SecurityContext';
import ResourceResponsive from '../resource/ResourceResponsive';
import {Button, Container, Form, Grid, Header, Segment} from "semantic-ui-react";

export default class ResourceStatistics extends React.Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            groups: {}
        };
    }

    componentDidMount() {
        const retrieve_url = this.context.security.is_reviewer || this.context.security.is_superuser ? 'retrieve-admin' : 'retrieve';
        const headers = {};
        if (this.context.security.token) {
            headers['Authorization'] = `Bearer ${this.context.security.token}`;
        }

        axios
            .get('/api/public/resource-stats')
            .then(res => {
                this.setState({
                    groups: res.data
                });
            });
    }

    render() {
        var stat_list = [];
        console.log(this.state.groups)
        for (var i = 0; i < this.state.groups.length; i+=1)
        {
            stat_list.push(<ResourceResponsive resource_component={<ResourceStatGroup group={this.state.groups[i]}/>}/>);
        }

        return (
            <Container>
                {stat_list}
            </Container>
        );
    }
}