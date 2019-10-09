import React, { Component } from 'react'

export class ResourceSubmitForm extends Component {
    render() {
        return (
            <div>
                <button type="button">{this.props.button_text}</button>
            </div>
        )
    }
}

export default ResourceSubmitForm
