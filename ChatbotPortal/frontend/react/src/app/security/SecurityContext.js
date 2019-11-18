import React from "react";
import axios from "axios";

export const refreshLoadingSecurityContext = (url, setSecurity) => {
        axios
            .get(url + 'currentuser/')
            .then(
                response => {
                    // if response.data !== null
                    if (response.data !== '') {
                        response.data['is_logged_in'] = true;
                        setSecurity(response.data);
                        // console.log(this.state.security.is_logged_in);
                    } else {
                        response.data = JSON.parse('{}');
                        response.data['is_logged_in'] = false;
                        setSecurity(response.data);
                        console.log(this.state.security.is_logged_in);
                    }
                },
                error => {
                    console.log(error);
                }
            );

    };

export const SecurityContext = React.createContext({
    /**
     * creating a security context
     */
    security: {},   // hold the value
    setSecurity: null, // allow changes to security
});

export class SecurityContextProvider extends React.Component {
    /**
     * A security context provider that provides context to every component
     * @param props properties that needs to be passed
     */
    BASE_AUTH_URL = 'http://127.0.0.1:8000/chatbotportal/authentication/';
    constructor(props) {
        /**
         * A constructor that sets the security as state
         */
        super(props);
        this.state = {
            security: {},
        }
    }

    setSecurity = (security) => {
        /**
         * A function that sets the sucurity
         */
        this.setState({
            security
        })
    };

    componentDidMount() {


        axios
            .get(this.BASE_AUTH_URL + 'currentuser/', {withCredentials: true})
            .then(
                response => {
                    // if response.data !== null
                    if (response.data !== '') {
                        response.data['is_logged_in'] = true;
                        this.setState({security: response.data});
                        console.log(this.state.security.is_logged_in);
                    } else {
                        response.data = JSON.parse('{}');
                        response.data['is_logged_in'] = false;
                        this.setState({security: response.data});
                        console.log(this.state.security.is_logged_in);
                    }
                },
                error => {
                    console.log(error);
                }
            );
    };
    render() {
        return(
            <SecurityContext.Provider value={{security : this.state.security, setSecurity : this.setSecurity}}>
                {this.props.children}
            </SecurityContext.Provider>
        )
    }
}



