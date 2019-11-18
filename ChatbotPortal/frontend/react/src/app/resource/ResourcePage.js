import React from "react";
import ResourceList from "./ResourceList";
import {SecurityContext} from "../security/SecurityContext";

export default class ResourcePage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <SecurityContext.Consumer>
                    {(securityContext) => (
                        <div>
                            {securityContext.security.is_logged_in ?
                                <ResourceList/>
                                : null}
                        </div>)}
                </SecurityContext.Consumer>
            </div>
        );
    }
}
