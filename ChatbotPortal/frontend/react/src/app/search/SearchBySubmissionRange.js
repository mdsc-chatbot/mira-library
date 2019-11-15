import React from 'react';
import {Form} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of submissions
 */
class SearchBySubmissionRange extends React.Component {

    state ={
        submission_range_option:"",
    }

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the parent state
     * @param e = event
     */
    handle_change_submission_range = e => {
        let name = e.target.name;
        let value = e.target.value;

        if (!!value) {
            this.props.set_submission_search_params({name, value})
        } else {
            value = "''";
            this.props.set_submission_search_params({name, value})
        }
    };

    handle_change_submission_range_option = (e, { value }) => {
        this.setState({ submission_range_option: value })
        let name = "submission_range_option"
        this.props.set_submission_search_params({ name, value })
    }

    /**
     * This function renders the form containing the input fields
     * @returns {*}
     */
    render() {
        return (
            <Form>
                <Form.Input
                    fluid
                    placeholder="Start Submission Number"
                    name="start_submission"
                    onChange={this.handle_change_submission_range}
                />
                <Form.Input
                    fluid
                    placeholder="End Submission Number"
                    name="end_submission"
                    onChange={this.handle_change_submission_range}
                />
                <Form.Checkbox
                    fluid
                    label="total"
                    name="submission_range_option"
                    value="total"
                    checked={this.state.submission_range_option === "total"}
                    onChange={this.handle_change_submission_range_option}
                    radio
                />
                <Form.Checkbox
                    fluid
                    label="pending"
                    name="submission_range_option"
                    value="pending"
                    checked={this.state.submission_range_option === "pending"}
                    onChange={this.handle_change_submission_range_option}
                    radio
                />
                <Form.Checkbox
                    fluid
                    label="approved"
                    name="submission_range_option"
                    value="approved"
                    checked={this.state.submission_range_option === "approved"}
                    onChange={this.handle_change_submission_range_option}
                    radio
                />
                <Form.Checkbox
                    fluid
                    label="reset"
                    name="submission_range_option"
                    value="''"
                    checked={this.state.submission_range_option === "''"}
                    onChange={this.handle_change_submission_range_option}
                    style={{paddingBottom:30}}
                    radio
                />
            </Form>
        );
    }
}

export default SearchBySubmissionRange;