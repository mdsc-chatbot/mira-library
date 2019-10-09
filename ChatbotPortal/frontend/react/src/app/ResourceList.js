import React, { Component } from 'react'
import axios from 'axios';

import ResourceListItem from './ResourceListItem.js'

export class ResourceList extends Component {

    state = {
        resources: []
    };
    
    fetchResources = () => {
    axios.get("http://127.0.0.1:8000/api/user/resources").then(res => {
        this.setState({
        resources: res.data
        });
        console.log(this.state.resources);
    });
    }

    componentDidMount() {
        this.fetchResources();
    }

    componentWillReceiveProps(newProps) {
    if (newProps.token) {
        this.fetchResources();      
    }
    }

    render() {

        return this.state.resources.map((resource) => (
            <Resource key={resource.id} resource={resource}/>
          ));
    }
}

export default ResourceList
