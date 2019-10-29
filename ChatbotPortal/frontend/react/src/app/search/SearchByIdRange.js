import React from 'react';
import {DatesRangeInput} from 'semantic-ui-calendar-react';
import {Button, Dropdown, Form} from 'semantic-ui-react'
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";

const dateOption = [
    {key: 'last_login', value: 'last_login', text: 'By Last Login'},
    {key: 'date_joined', value: 'date_joined', text: 'By Creation Date'}
];

/**
 * This class helps searching the users by a range of dates
 */
class SearchByIdRange extends React.Component {

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
            is_logged_in: false,
            value: 'last_login',
            datesRange: ''
        };
    }

    /**
     * This function gets called when the the component gets mounted
     */
    componentDidMount() {
        this.updateStateFromSecurityContext();
    }

    /**
     * This function is called when either the state or the props or both get updated
     */
    componentDidUpdate() {
        this.updateStateFromSecurityContext();

    }

    /**
     * This function updates the state from the security context
     */
    updateStateFromSecurityContext = () => {
        if (this.state.is_logged_in === false && this.context.security && this.context.security.is_logged_in) {
            this.setState({
                is_logged_in: this.context.security.is_logged_in
            });
        }
    };

    /**
     * This function executes the query by calling backend controller (API),
     * which returns the users who have the defined date characteristics.
     * @param e = event
     * @param searchFormData = Data received from search form
     */
    handle_search = (e, searchFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();
        if (this.context.security.is_logged_in) {
            // Split the datesRanges into two dates
            const date_range = searchFormData.datesRange.split(' - ');

            // The backend URL
            const url = `http://127.0.0.1:8000/authentication/super/search/date_range/${searchFormData.value}/${date_range[0]}/${date_range[1]}/`;

            // Having the permission header loaded
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };

            /**
             * Calling the backend API
             */
            axios
                .get(url, {headers: options})
                .then(
                    response => {
                        // console.log(response.data);
                        this.setState({

                            // Setting the response in user state
                            users: response.data,
                        });
                    },
                    error => {
                        console.log(error);
                    }
                )
        }
    };

    /**
     * This function handles the changes that happen to in the date range field of the form.
     * @param event
     * @param name = Name of the state
     * @param value = Value of the state
     */
    handle_change_dateRange = (event, {name, value}) => {
        if (this.state.hasOwnProperty(name)) {
            this.setState({[name]: value});
        }
    };

    /**
     * This function handles the changes that happen to in the drop down field of the form.
     * @param e = Event
     * @param value = The value from the drop down form that will be stored in the state
     */
    handle_change_dropdown = (e, {value}) => {
        this.setState({value})
    };

    /**
     * This function renders the form containing the DateRangeInput and Dropdown menus
     * @returns {*}
     */
    render() {
        return (
            <SecurityContext.Consumer>
                {(securityContext) => (
                    <Form onSubmit={e => this.handle_search(e, this.state)}>
                        <DatesRangeInput
                            name="datesRange"
                            placeholder="From - To"
                            value={this.state.datesRange}
                            iconPosition="left"
                            onChange={this.handle_change_dateRange}
                            dateFormat={"YYYY-MM-DD"}
                        />

                        <Dropdown
                            search
                            searchInput={{ type: 'number' }}
                            selection
                            placeholder='Select ID...'
                        />

                        {securityContext.security.is_logged_in ? (
                            <Button
                                color="blue"
                                fluid size="large">
                                Search
                            </Button>
                        ) : null}
                    </Form>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default SearchByIdRange;