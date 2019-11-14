import React from 'react';
import {Form} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of submissions
 */
class SearchBySubmissionRange extends React.Component {

    state ={
        pending: false,
        approved:false,
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

    handle_pending_change = () => {
        this.setState(({ pending }) => ({ pending: !pending }));
    }

    handle_approved_change = () => {
        this.setState(({ approved }) => ({ approved: !approved }));
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
                    label="Pending resource submission"
                    name="pending"
                    checked={this.state.pending}
                    onChange={this.handle_pending_change}
                />
                <Form.Checkbox
                    fluid
                    label="Approved resource submission"
                    name="approved"
                    checked={this.state.approved}
                    onChange={this.handle_approved_change}
                    style={{paddingBottom:30}}
                />
            </Form>
        );
    }
}

export default SearchBySubmissionRange;