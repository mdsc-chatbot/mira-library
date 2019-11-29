/**
 * @file: MenuContext.js
 * @summary: A react context that allows different menu header for extension and the regular website
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

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

    /**
     * Set up the state for menu context
     * @param menu_visibility: boolean
     */
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



