import React from "react";

const SecurityInternalContext = React.createContext({
    security: {},
    setSecurity: null,
});

export class SecurityContext extends React.Component {
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
            <SecurityInternalContext.Provider value={{security : this.state.security, setSecurity : this.setSecurity}}>
                {children}
            </SecurityInternalContext.Provider>
        )
    }
}



