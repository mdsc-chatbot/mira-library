/**
 * @file: CategoryDropDown.js
 * @summary: Drop down component for categories (Website, Video, PDF), used in ResourceSubmitForm.js
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
import axios from 'axios';
import PropTypes from 'prop-types';
import {Dropdown} from 'semantic-ui-react';
import { SecurityContext } from "../contexts/SecurityContext";


export default class CategoryDropdown extends React.Component {
    static contextType = SecurityContext;

    static propTypes = {
        value : PropTypes.string,
        onChange : PropTypes.func.isRequired,
    };

    constructor(props) {
        super(props);

        this.state = {
            options : []
        }
    }

    componentDidMount() {
        // Fetch options for dropdown
        axios
            .get("/chatbotportal/resource/fetch-categories", {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(response => {
                this.setState({
                    options: response.data.map(category => ({
                        key: category.id,
                        value: category.id,
                        text: category.name
                    }))
                });

                this.setState({
                    options: this.state.options.sort((a, b) => a.text.localeCompare(b.text))
                })
            });
    }

    handleChange = (event, data) => {
        this.props.onChange(data.value);
    };

    componentDidUpdate(prevProps) {
        if (prevProps.catText !== this.props.catText) {
            const newValue = this.state.options.filter(option=>option.text==this.props.catText)[0].value;
            this.props.onChange(newValue);
        }
    }

    render() {
        return (
            <Dropdown
                fluid
                selection
                options={this.state.options}
                onChange={this.handleChange}
                value={this.props.value}
            />
        );
    };
}