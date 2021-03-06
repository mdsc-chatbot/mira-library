/**
 * @file: SearchByDateRange.js
 * @summary: Renders the form that allows the user to interact with airbnb calendar and select the date options
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
import {Container, Dropdown, Form, Popup, Segment} from 'semantic-ui-react'
import {DateRangePicker} from "react-dates";
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';

const dateOption = [
    {key: 'unselected', value: "''", text: 'Unselected'},
    {key: 'last_login', value: 'last_login', text: 'By Last Login'},
    {key: 'date_joined', value: 'date_joined', text: 'By Creation Date'}
];

/**
 * This class helps searching the users by a range of dates
 */
class SearchByDateRange extends React.Component {

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{datesRange: string, value: string}}
         */
        this.state = {
            datesRange: '',

            startDate: '',
            endDate: '',
            focusedInput: null

        };
    }

    /**
     * This function handles the changes that happen to in the date range field of the form.
     * @param event
     * @param name = Name of the state
     * @param value = Value of the state
     */
    handle_change_daterange = (event, {name, value}) => {
        this.setState({[name]: value});
        if (!!value) {
            const date_range = value.split(' - ');
            this.props.set_date_range_params(date_range[0], date_range[1])
        } else {
            value = "'' - ''";
            const date_range = value.split(' - ');
            this.props.set_date_range_params(date_range[0], date_range[1])
        }
    };

    /**
     * Handles the changes to the date range picker and sets the date into props and the states
     * @param startDate
     * @param endDate
     */
    handle_date_change = ({startDate, endDate}) => {
        console.log(startDate)
        if (startDate === '' || startDate === null || endDate === '' || endDate === null) {
            this.props.set_date_range_params('', '')
        } else {
            this.props.set_date_range_params(startDate.format('YYYY-MM-DD'), endDate.format('YYYY-MM-DD'))
        }
        this.setState({
            startDate: startDate,
            endDate: endDate
        });

    };

    /**
     * This function handles the changes that happen to in the drop down field of the form.
     * @param e = Event
     * @param value = The value from the drop down form that will be stored in the state
     */
    handle_change_dropdown = (e, {value}) => {
        // this.setState({value});
        this.props.set_date_option_params(value);
    };

    /**
     * This function renders the form containing the DateRangeInput and Dropdown menus
     * @returns {*}
     */
    render() {
        return (
            <Form size="mini">
                <Container content="Date option"/>
                <Dropdown
                    name='date_option_dropdown'
                    placeholder='Unselected'
                    fluid
                    search
                    selection
                    onChange={this.handle_change_dropdown}
                    options={dateOption}
                />
                <Segment id="date_popup" size={"mini"}>
                    <Popup flowing hoverable position={"top right"} size={"mini"}
                           trigger={<Container content="Date range"/>}>
                        <DateRangePicker
                            endDate={this.state.endDate}
                            focusedInput={this.state.focusedInput}
                            initialEndDate={null}
                            initialStartDate={null}
                            initialVisibleMonth={null}
                            isDayBlocked={function noRefCheck() {
                            }}
                            isDayHighlighted={function noRefCheck() {
                            }}
                            isOutsideRange={function noRefCheck() {
                            }}
                            numberOfMonths={1}
                            onDatesChange={({startDate, endDate}) => this.handle_date_change({startDate, endDate})}
                            onFocusChange={focusedInput => this.setState({focusedInput})}
                            showClearDates
                            small
                            startDate={this.state.startDate}
                        />
                    </Popup>
                </Segment>
            </Form>
        );
    }
}

export default SearchByDateRange;