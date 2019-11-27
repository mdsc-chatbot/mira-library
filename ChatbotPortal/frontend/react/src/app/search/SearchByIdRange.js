/**
 * @file: SearchByIdRange.js
 * @summary: Renders the form that allows the user to request search based on a range of user ids
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
import {Form, FormGroup, FormInput} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of ids
 */
class SearchByIdRange extends React.Component {

    /**
     * This function handles any changes that happens to the form fields
     * and alters the parent props.
     * @param e = event
     */
    handle_change = e => {
        let name = e.target.name;
        let value = e.target.value;
        if (!!value) {
            this.props.set_id_search_params({name, value})
        } else {
            value = "''";
            this.props.set_id_search_params({name, value})
        }
    };

    /**
     * This function renders the form containing the input fields
     * @returns {*}
     */
    render() {
        return (
            <Form size="mini">
                <FormGroup>
                <FormInput
                    fluid
                    placeholder="Start ID"
                    name="start_id"
                    onChange={this.handle_change}
                    size="mini"
                />
                <FormInput
                    fluid
                    placeholder="End ID"
                    name="end_id"
                    onChange={this.handle_change}
                    size="mini"
                />
                </FormGroup>
            </Form>
        );
    }
}

export default SearchByIdRange;