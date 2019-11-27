import React from "react";

/**
 * creating a menu context that will allow us to decide
 * whether a menu bar is to show or not
 * @type {React.Context<{menu_visibility: boolean}>}
 */
export const MenuContext = React.createContext({
    menu_visibility: true
});

export class MenuContextProvider extends React.Component {
    /**
     * A menu context provider that provides context to every component
     * @param props properties that needs to be passed
     */
    constructor(props) {
        /**
         * A constructor that sets the menu as state
         */
        super(props);
        this.state = {
            menu_visibility: true,
        }
    }

    set_menu_visibility = (menu_visibility) => {
        this.setState({menu_visibility})
    };

    /**
     * Rendering the Menu context provider to the rest of the app
     * @returns {*}
     */
    render() {
        return (
            <MenuContext.Provider value={{
                menu_visibility: this.state.menu_visibility,
                set_menu_visibility : this.set_menu_visibility
            }}>
                {this.props.children}
            </MenuContext.Provider>
        )
    }
}



