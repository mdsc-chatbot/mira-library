import React, { Component } from 'react'

import ResourceList from './ResourceList'
import ResourceSubmitForm from './ResourceSubmitForm'

export class ResourcePage extends Component {
    
    render() {
        return (        
			<div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
				<h2> Resources List </h2>
				{/* <ResourceSubmitForm request_type="post" articleID={null} button_text="Create" /> */}
				<ResourceList />
			</div>
        )
    }
}

export default ResourcePage
