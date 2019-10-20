import React from "react";

export const SecurityContext = React.createContext({
    security: {},
    setSecurity: null,
});

export class SecurityContextProvider extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            security: {},
        }
    }

    setSecurity = (security) => {
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



