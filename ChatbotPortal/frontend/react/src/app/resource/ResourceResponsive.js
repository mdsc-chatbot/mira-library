import React, { Component } from "react";
import { Responsive } from "semantic-ui-react";

export class ResourceResponsive extends Component {
    render() {
        return (
            <div>
                <Responsive {...Responsive.onlyMobile}>
                    <div style={{ paddingTop: 30, paddingLeft: 15, paddingRight: 15, paddingBottom: 30 }}>
                        {this.props.resource_component}
                    </div>
                </Responsive>
                <Responsive minWidth={768}>
                    <div style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30 }}>
                        {this.props.resource_component}
                    </div>
                </Responsive>
            </div>
        );
    }
}

export default ResourceResponsive;
