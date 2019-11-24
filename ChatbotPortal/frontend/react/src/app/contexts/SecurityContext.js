import React from "react";
import axios from "axios";
import PropTypes from "prop-types";
import {withRouter} from 'react-router';

/**
 * creating a security context
 * @type {React.Context<{security: {}, setSecurity: null}>}
 */
export const SecurityContext = React.createContext({
    security: {},
    setSecurity: null
});

class InnerSecurityContextProvider extends React.Component {

    static propTypes = {
        // From withRouter
        location : PropTypes.object,
    };

    /**
     * A security context provider that provides context to every component
     * @param props properties that needs to be passed
     */
    constructor(props) {
        /**
         * A constructor that sets the security as state
         */
        super(props);
        this.state = {
            security: {},
        };
    }

    /**
     * A function that sets the sucurity
     * @param security
     */
    setSecurity = (security) => {
        this.setState({
            security
        })
    };

    /**
     * This function gets the current logged in user from the backend using session id
     */
    get_the_current_user = () => {

        axios
            .get('/chatbotportal/authentication/currentuser/', {withCredentials: true})
            .then(
                response => {
                    /**
                     * If the response data is not empty set is_logged_in status to true, otherwise false
                     */
                    if (response.data !== '') {
                        response.data['is_logged_in'] = true;
                        this.setState({security: response.data});
                    } else {
                        response.data = JSON.parse('{}');
                        response.data['is_logged_in'] = false;
                        this.setState({security: response.data});
                    }
                },
                error => {
                    console.log(error);
                }
            );
    };

    /**
     * Get the corrent user once the security context is mounted
     *
     * Only get the current user if not using a certain url (i.e. resource submission through extension)
     * We use the component UpdateContexts to update the context.
     */
    componentDidMount() {
        if (!this.props.location.pathname.startsWith('/chatbotportal/app/resource_submit/extension/')) {
            this.get_the_current_user();
        }
    };

    /**
     * Render the SecurityContext provider to the rest of the app
     * @returns {*}
     */
    render() {
        return(
            <SecurityContext.Provider value={{security : this.state.security, setSecurity : this.setSecurity}}>
                {this.props.children}
            </SecurityContext.Provider>
        )
    }
}

export const SecurityContextProvider = withRouter(InnerSecurityContextProvider);