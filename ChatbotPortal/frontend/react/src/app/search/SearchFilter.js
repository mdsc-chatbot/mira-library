/**
 * @file: SearchFilter.js
 * @summary: Renders the form that allows the user to search based on filters such as is_active, is_reviewer, is_staff
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
import {Form, Container, Dropdown, Responsive} from "semantic-ui-react";

const options = [
    {key: 1, text: 'Yes', value: 'true'},
    {key: 2, text: 'No', value: 'false'},
    {key: 3, text: 'None', value: "''"},
];

/**
 * This class helps filtering users based on either is_active or is_reviewer or is_staff
 */
class SearchFilter extends React.Component {

    /**
     * This function handles the changes in the drop down and alters the parent props
     * @param name = name of the drop down
     * @param value = value from the options
     */
    handle_change_dropdown = ({name, value}) => {
        if (!!value) {
            this.props.set_status_search_params({name, value});
        } else {
            value = "''";
            this.props.set_status_search_params({name, value});
        }
    };

    /**
     * This function renders the form containing the Dropdown options
     * @returns {*}
     */
    render() {
        return (
            <Form size='mini'>
                <Container content='Active'/>
                <Dropdown
                    name='is_active'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
                <Container content='Reviewer'/>
                <Dropdown
                    name='is_reviewer'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
                <Container content='Staff'/>
                <Dropdown
                    name='is_staff'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
            </Form>
        );
    }
}

export default SearchFilter;
