import React from 'react';
import {DatesRangeInput} from 'semantic-ui-calendar-react';
import {Button, Form, Segment} from 'semantic-ui-react'
import axios from "axios";

class SearchByDateRange extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            datesRange: ''
        };
    }

    handle_search = (e, searchFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();
    };

    handleChange = (event, {name, value}) => {
        if (this.state.hasOwnProperty(name)) {
            this.setState({[name]: value});
        }
    }

    render() {
        return (
            <Form>
                <DatesRangeInput
                    name="datesRange"
                    placeholder="From - To"
                    value={this.state.datesRange}
                    iconPosition="left"
                    onChange={this.handleChange}
                    dateFormat={"YYYY-MM-DD"}
                />

                <Button
                    color="blue"
                    fluid size="large">
                    Search
                </Button>
            </Form>
        );
    }
}

export default SearchByDateRange;