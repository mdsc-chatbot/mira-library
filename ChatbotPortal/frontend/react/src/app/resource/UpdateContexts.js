import React, {Component, useCallback} from "react";
import {SecurityContext} from "../contexts/SecurityContext";

class UpdateContexts extends Component {
    static contextType = SecurityContext;

    componentDidMount() {
        this.context.setSecurity({
            is_logged_in: true,
            token: this.props.token
        });
    }

    componentDidUpdate(prevProps) {
        if (prevProps.token !== this.props.token) {
            this.context.setSecurity({
                token: this.props.token
            });
        }
    }

    render() {
        return (
            <div/>
        );
    }
}

export default UpdateContexts