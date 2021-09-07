
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


export default class ResourceFormatDropdown extends React.Component {
    static contextType = SecurityContext;

    static propTypes = {
        value : PropTypes.string,
        onChange : PropTypes.func.isRequired,
    };

    PROGRAMS_AND_SERVICES =[
        'Addiction and recovery',
        'Clinical Inpatient Mental Health',
        'Clinical Outpatient Mental Health',
        'Community Support',
        'Crisis Support/Distress Counselling',
        'Family Doctor',
        'Group therapy',
        'Housing - Emergency',
        'Housing - Long term',
        'Legal Counselling',
        'Medical services',
        'Newsletter',
        'Online chat',
        'Peer Support',
        'Pets - Boarding and care',
        'Phone',
        'Psychiatrist',
        'Psychologist',
        'Rehabilitation',
        'Short term treatment',
        'Text',
        'Therapist/Counsellor/Psychotherapist',
        'Traditional Indigenous Healeer',
        'Violence intervention'
    ];

    EDUCATIONAL_INFORMATIONAL =[
        'Classes/course (in person)',
        'Definition',
        'Email newsletter',
        'Forum',
        'Mobile App',
        'Online course (asynchronous)',
        'Online course (synchronous)',
        'Online screening tool',
        'Podcast/audio recording',
        'Statistic',
        'Subtitles',
        'Symptoms',
        'Training',
        'Transcript',
        'Treatments',
        'Video',
        'Webinar (asynchronous)',
        'Webinar (synchronous)',
        'Worksheet'
    ];

    constructor(props) {
        super(props);

        this.state = {
            options : [],
        }
    }

    // Fetch options for dropdown
    componentDidMount() {
        const prevOptions = this.state.options;
        var serviceOptions = [];
        if(this.props.is_informational=='RS'){
            this.EDUCATIONAL_INFORMATIONAL.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }else if(this.props.is_informational=='SR'){
            this.PROGRAMS_AND_SERVICES.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }else{
            this.PROGRAMS_AND_SERVICES.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
            this.EDUCATIONAL_INFORMATIONAL.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }
        serviceOptions.sort((a, b) => a.key.localeCompare(b.key))
        if(prevOptions.length != serviceOptions.length){
            this.setState({options: serviceOptions});
        }
    }

     // Fetch options for dropdown
    componentDidUpdate() { 
        const prevOptions = this.state.options;
        var serviceOptions = [];
        if(this.props.is_informational=='RS'){
            this.EDUCATIONAL_INFORMATIONAL.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }else if(this.props.is_informational=='SR'){
            this.PROGRAMS_AND_SERVICES.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }else{
            this.PROGRAMS_AND_SERVICES.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
            this.EDUCATIONAL_INFORMATIONAL.forEach(element => {
                serviceOptions.push({
                    key: element,
                    text: element,
                    value: element
                });
            });
        }

        serviceOptions.sort((a, b) => a.key.localeCompare(b.key))

        if(prevOptions.length != serviceOptions.length){
            this.setState({options: serviceOptions});
        }
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

