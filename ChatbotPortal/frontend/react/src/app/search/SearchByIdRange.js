import React from 'react';
import {Form} from 'semantic-ui-react'


/**
 * This class helps searching the users by a range of ids
 */
class SearchByIdRange extends React.Component {

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{start_id: string, end_id: string}}
         */
        this.state = {
            start_id: "''",
            end_id: "''",
        };
    }

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        let name = e.target.name;
        let value = e.target.value;

        if (!!value){
            this.props.set_id_search_params({name, value})
        } else {
            value = "''";
            this.props.set_id_search_params({name, value})
        }

        this.setState(prevstate => {
            const newState = {...prevstate};
            newState[name] = value;
            return newState;
        });
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
                    placeholder="Start ID"
                    name="start_id"
                    onChange={this.handle_change}
                />
                <Form.Input
                    fluid
                    placeholder="End ID"
                    name="end_id"
                    onChange={this.handle_change}
                />
            </Form>
        );
    }
}

export default SearchByIdRange;