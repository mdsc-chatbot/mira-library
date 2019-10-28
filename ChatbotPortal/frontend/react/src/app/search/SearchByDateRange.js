import React from 'react';
import {DatesRangeInput} from 'semantic-ui-calendar-react';
import {Form} from 'semantic-ui-react'

class SearchByDateRange extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            date: '',
            time: '',
            dateTime: '',
            datesRange: ''
        };
    }

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
            </Form>
        );
    }
}

export default SearchByDateRange;