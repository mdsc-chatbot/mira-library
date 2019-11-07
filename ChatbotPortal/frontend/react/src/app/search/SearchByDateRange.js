import React from 'react';
import {DatesRangeInput} from 'semantic-ui-calendar-react';
import {Dropdown, Form} from 'semantic-ui-react'
import {SecurityContext} from "../security/SecurityContext";

const dateOption = [
    {key: 'last_login', value: 'last_login', text: 'By Last Login'},
    {key: 'date_joined', value: 'date_joined', text: 'By Creation Date'}
];

/**
 * This class helps searching the users by a range of dates
 */
class SearchByDateRange extends React.Component {

    static contextType = SecurityContext;

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
            value: "''",
            datesRange: ''
        };
    }

    componentDidMount() {
        this.props.set_date_option_params(this.state.value);
    }

    /**
     * This function handles the changes that happen to in the date range field of the form.
     * @param event
     * @param name = Name of the state
     * @param value = Value of the state
     */
    handle_change_daterange = (event, {name, value}) => {
        if (this.state.hasOwnProperty(name)) {
            this.setState({[name]: value});
        }

        const date_range = value.split(' - ');

        this.props.set_date_range_params(date_range[0], date_range[1])
    };

    /**
     * This function handles the changes that happen to in the drop down field of the form.
     * @param e = Event
     * @param value = The value from the drop down form that will be stored in the state
     */
    handle_change_dropdown = (e, {value}) => {
        this.setState({value});
        this.props.set_date_option_params(value);
    };

    /**
     * This function renders the form containing the DateRangeInput and Dropdown menus
     * @returns {*}
     */
    render() {
        return (
            <Form onSubmit={e => this.handle_search(e, this.state)}>
                <DatesRangeInput
                    name="datesRange"
                    placeholder="From - To"
                    value={this.state.datesRange}
                    iconPosition="left"
                    onChange={this.handle_change_daterange}
                    dateFormat={"YYYY-MM-DD"}
                />

                <Dropdown
                    placeholder='Date of ...'
                    fluid
                    search
                    selection
                    onChange={this.handle_change_dropdown}
                    options={dateOption}
                />
            </Form>
        );
    }
}

export default SearchByDateRange;