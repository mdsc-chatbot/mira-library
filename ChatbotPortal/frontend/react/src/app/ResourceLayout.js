import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Layout, Menu, Breadcrumb } from 'antd';
const { Header, Content, Footer } = Layout;

import ResourceList from './ResourceList'
import ResourceSubmitForm from './ResourceSubmitForm'

export class ResourceLayout extends Component {
    
    render() {
        return (
            <Layout>
                <Header>
                    <Menu></Menu>
                    
                 </Header>

                 <Content style={{ padding: '0 50px' }}>
                    
                    <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
                        <h2> Resources List </h2>
                        <ResourceSubmitForm request_type="post" articleID={null} button_text="Create" />
                        <ResourceList />
                    </div>
                </Content>
        
            </Layout>
        )
    }
}

export default ResourceLayout
