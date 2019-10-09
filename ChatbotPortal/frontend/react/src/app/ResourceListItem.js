import React, { Component } from 'react'

export class ResourceListItem extends Component {
    render() {
        const resource = this.props.resource

        return (
            <p>
                <a href={`/chatbotportal/${resource.id}/`}>{resource.title}</a>
            </p>
        )
    }
}

export default ResourceListItem
