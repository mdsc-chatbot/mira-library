import React, { Component } from 'react'
import axios from 'axios';

export class ResourceDetail extends Component {
    state = {
        resource: {}
      };
    
    componentDidMount() {
      const resourceID = this.props.match.params.resourceID;
      axios.get(`http://127.0.0.1:8000/api/user/resources/${resourceID}`).then(res => {
        this.setState({
          resource: res.data
        });
      });
    }

    render() {

        return (
            <div>
                <p> TITLE: {this.state.resource.title} URL: {this.state.resource.url}</p>
            </div>
        )
    }
}

export default ResourceDetail
