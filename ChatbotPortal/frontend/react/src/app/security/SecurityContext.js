import React from "react";

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

    render() {
        return(
            <SecurityContext.Provider value={{security : this.state.security, setSecurity : this.setSecurity}}>
                {this.props.children}
            </SecurityContext.Provider>
        )
    }
}



