import React from 'react';
import {Form} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of submissions
 */
class SearchBySubmissionRange extends React.Component {

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
            </Form>
        );
    }
}

export default SearchBySubmissionRange;