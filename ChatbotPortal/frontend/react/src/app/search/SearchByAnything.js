/**
 * @file: SearchByAnything.js
 * @summary: Renders the input field required for search by anything option
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

import React from 'react';
import {Form, FormInput} from 'semantic-ui-react'


/**
 * This class helps searching the users by any attribute
 */
class SearchByAnything extends React.Component {

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{item: string}}
         */
        this.state = {
            search_string: "''"
        };
    }

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        let name = e.target.name;
        let value = e.target.value;

        this.props.set_search_string({name, value});

        this.setState(prevstate => {
            const newState = {...prevstate};
            newState[name] = value;
            return newState;
        });
    };

    /**
     * This function renders the form containing the search input field
     * @returns {*}
     */
    render() {
        return (
                <FormInput
                    fluid
                    placeholder="Search by any attribute ..."
                    name="search_string"
                    onChange={this.handle_change}
                    size='small'
                />

        );
    }
}

export default SearchByAnything;