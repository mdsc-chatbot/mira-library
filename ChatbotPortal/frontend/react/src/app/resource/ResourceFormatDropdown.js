
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
        if(!this.props.is_informational=='RS'){
            serviceOptions = [
                {
                    key: 'definition',
                    text: 'definition',
                    value: 'definition'
                },
                {
                    key: 'statistic',
                    text: 'statistic',
                    value: 'statistic'
                },
                {
                    key: 'symptoms',
                    text: 'symptoms',
                    value: 'symptoms'
                },
                {
                    key: 'treatments',
                    text: 'treatments',
                    value: 'treatments'
                }
            ];
        }else if(this.props.is_informational=='SR'){
            serviceOptions = [
                {
                    key: 'peer-support',
                    text: 'peer-support',
                    value: 'peer-support'
                },
                {
                    key: 'crisis support/distress counselling',
                    text: 'crisis support/distress counselling',
                    value: 'crisis support/distress counselling'
                },
                {
                    key: 'online course/webinar',
                    text: 'online course/webinar',
                    value: 'online course/webinar'
                },
                {
                    key: 'Therapist/Counsellor',
                    text: 'Therapist/Counsellor',
                    value: 'Therapist/Counsellor'
                },
                {
                    key: 'Psychologist',
                    text: 'Psychologist',
                    value: 'Psychologist'
                },
                {
                    key: 'Family Doctor',
                    text: 'Family Doctor',
                    value: 'Family Doctor'
                }
            ];
        }else{
            serviceOptions = [
                {
                    key: 'peer-support',
                    text: 'peer-support',
                    value: 'peer-support'
                },
                {
                    key: 'crisis support/distress counselling',
                    text: 'crisis support/distress counselling',
                    value: 'crisis support/distress counselling'
                },
                {
                    key: 'online course/webinar',
                    text: 'online course/webinar',
                    value: 'online course/webinar'
                },
                {
                    key: 'Therapist/Counsellor',
                    text: 'Therapist/Counsellor',
                    value: 'Therapist/Counsellor'
                },
                {
                    key: 'Psychologist',
                    text: 'Psychologist',
                    value: 'Psychologist'
                },
                {
                    key: 'Family Doctor',
                    text: 'Family Doctor',
                    value: 'Family Doctor'
                },
                {
                    key: 'definition',
                    text: 'definition',
                    value: 'definition'
                },
                {
                    key: 'statistic',
                    text: 'statistic',
                    value: 'statistic'
                },
                {
                    key: 'symptoms',
                    text: 'symptoms',
                    value: 'symptoms'
                },
                {
                    key: 'treatments',
                    text: 'treatments',
                    value: 'treatments'
                }
            ];
        }
        if(prevOptions.length != serviceOptions.length){
            this.setState({options: serviceOptions});
        }
    }

     // Fetch options for dropdown
    componentDidUpdate() { 
        const prevOptions = this.state.options;
        var serviceOptions = [];
        if(!this.props.is_informational=='RS'){
            serviceOptions = [
                {
                    key: 'definition',
                    text: 'definition',
                    value: 'definition'
                },
                {
                    key: 'statistic',
                    text: 'statistic',
                    value: 'statistic'
                },
                {
                    key: 'symptoms',
                    text: 'symptoms',
                    value: 'symptoms'
                },
                {
                    key: 'treatments',
                    text: 'treatments',
                    value: 'treatments'
                }
            ];
        }else if(this.props.is_informational=='SR'){
            serviceOptions = [
                {
                    key: 'peer-support',
                    text: 'peer-support',
                    value: 'peer-support'
                },
                {
                    key: 'crisis support/distress counselling',
                    text: 'crisis support/distress counselling',
                    value: 'crisis support/distress counselling'
                },
                {
                    key: 'online course/webinar',
                    text: 'online course/webinar',
                    value: 'online course/webinar'
                },
                {
                    key: 'Therapist/Counsellor',
                    text: 'Therapist/Counsellor',
                    value: 'Therapist/Counsellor'
                },
                {
                    key: 'Psychologist',
                    text: 'Psychologist',
                    value: 'Psychologist'
                },
                {
                    key: 'Family Doctor',
                    text: 'Family Doctor',
                    value: 'Family Doctor'
                }
            ];
        }else{
            serviceOptions = [
                {
                    key: 'peer-support',
                    text: 'peer-support',
                    value: 'peer-support'
                },
                {
                    key: 'crisis support/distress counselling',
                    text: 'crisis support/distress counselling',
                    value: 'crisis support/distress counselling'
                },
                {
                    key: 'online course/webinar',
                    text: 'online course/webinar',
                    value: 'online course/webinar'
                },
                {
                    key: 'Therapist/Counsellor',
                    text: 'Therapist/Counsellor',
                    value: 'Therapist/Counsellor'
                },
                {
                    key: 'Psychologist',
                    text: 'Psychologist',
                    value: 'Psychologist'
                },
                {
                    key: 'Family Doctor',
                    text: 'Family Doctor',
                    value: 'Family Doctor'
                },
                {
                    key: 'definition',
                    text: 'definition',
                    value: 'definition'
                },
                {
                    key: 'statistic',
                    text: 'statistic',
                    value: 'statistic'
                },
                {
                    key: 'symptoms',
                    text: 'symptoms',
                    value: 'symptoms'
                },
                {
                    key: 'treatments',
                    text: 'treatments',
                    value: 'treatments'
                }
            ];
        }

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

