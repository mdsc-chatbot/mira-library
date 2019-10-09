import React, { Component } from 'react'

export class ResourceListItem extends Component {
    render() {
        const resource = this.props.resource

        return (
            <p>
                <a href={`http://127.0.0.1:8000/api/user/resources/${resource.id}`}>{resource.title}</a>
            </p>
        )
    }
}

export default ResourceListItem
