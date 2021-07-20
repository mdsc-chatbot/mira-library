
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


export default class ResourceTypeDropdown extends React.Component {
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
        const serviceOptions = [
            {
                key: 'SR',
                text: 'Program/Service',
                value: 'SR'
            },
            {
                key: 'RS',
                text: 'Educational/Informational',
                value: 'RS'
            },
            {
                key: 'BT',
                text: 'Both a Program/Service and Educational/Informational',
                value: 'BT'
            }
        ];
        this.setState({options: serviceOptions});
    }

    handleChange = (event, data) => {
        this.props.onChange(data.value);
    };

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