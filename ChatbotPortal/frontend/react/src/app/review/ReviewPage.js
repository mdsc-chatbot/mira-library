import React from 'react';
import ReviewTable from './ReviewTable';
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
                        <container>
                            {securityContext.security.is_logged_in ?
                                <ReviewTable/>
                                : null}
                        </container>
                    )}
                </SecurityContext.Consumer>
            </div>
        );
    }
}