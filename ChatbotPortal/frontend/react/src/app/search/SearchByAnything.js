import React from 'react';
import {Form, FormInput} from 'semantic-ui-react'


/**
 * This class helps searching the users by any attribute
 */
class SearchByAnything extends React.Component {

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{item: string}}
         */
        this.state = {
            search_string: "''"
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

        this.props.set_search_string({name, value});

        this.setState(prevstate => {
            const newState = {...prevstate};
            newState[name] = value;
            return newState;
        });
    };

    /**
     * This function renders the form containing the search input field
     * @returns {*}
     */
    render() {
        return (
                <FormInput
                    fluid
                    placeholder="Search by any attribute ..."
                    name="search_string"
                    onChange={this.handle_change}
                    size='small'
                />

        );
    }
}

export default SearchByAnything;