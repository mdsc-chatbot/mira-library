import React from 'react';
import {DatesRangeInput} from 'semantic-ui-calendar-react';
import {Container, Dropdown, Form} from 'semantic-ui-react'

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
            datesRange: ''
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
                <Container content="Date range"/>
                <DatesRangeInput
                    closeOnMouseLeave
                    popupPosition="bottom left"
                    name="datesRange"
                    placeholder="From - To"
                    value={this.state.datesRange}
                    iconPosition="left"
                    onChange={this.handle_change_daterange}
                    dateFormat={"YYYY-MM-DD"}
                    pickerWidth={"50px"}
                />
            </Form>
        );
    }
}

export default SearchByDateRange;