import React from 'react';
import {Form, FormGroup, FormInput} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of ids
 */
class SearchByIdRange extends React.Component {

    /**
     * This function handles any changes that happens to the form fields
     * and alters the parent props.
     * @param e = event
     */
    handle_change = e => {
        let name = e.target.name;
        let value = e.target.value;
        if (!!value) {
            this.props.set_id_search_params({name, value})
        } else {
            value = "''";
            this.props.set_id_search_params({name, value})
        }
    };

    /**
     * This function renders the form containing the input fields
     * @returns {*}
     */
    render() {
        return (
            <Form size="mini">
                <FormGroup>
                <FormInput
                    fluid
                    placeholder="Start ID"
                    name="start_id"
                    onChange={this.handle_change}
                    size="mini"
                />
                <FormInput
                    fluid
                    placeholder="End ID"
                    name="end_id"
                    onChange={this.handle_change}
                    size="mini"
                />
                </FormGroup>
            </Form>
        );
    }
}

export default SearchByIdRange;