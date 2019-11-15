import React, { Component } from 'react'
import { Icon } from "semantic-ui-react";

export class ResourceReviewStatus extends Component {
    render() {
        return (
            <div>
                {this.props.resource.review_status === "approved" &&
                    <Icon name="check" color="green" />
                }
                {this.props.resource.review_status === "rejected" &&
                    <Icon name="x" color="red" />
                }
                {this.props.resource.review_status === "pending" &&
                    <Icon name="sync alternate" color="yellow" />
                }
            </div>
        )
    }
}

export default ResourceReviewStatus
