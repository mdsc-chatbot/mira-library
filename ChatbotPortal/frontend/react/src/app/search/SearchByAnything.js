import React from 'react';
import {Button, Form} from 'semantic-ui-react'
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";


/**
 * This class helps searching the users by any attribute
 */
class SearchByAnything extends React.Component {

    static contextType = SecurityContext;

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{item: string, is_logged_in: boolean}}
         */
        this.state = {
            is_logged_in: false,
            item: ''
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
     * which returns the users who have the defined attribute characteristics.
     * @param e = event
     * @param searchFormData = Data received from search form
     */
    handle_search = (e, searchFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();
        if (this.context.security.is_logged_in) {
            // The backend URL
            const url = `http://127.0.0.1:8000/authentication/super/search/by_anything/?search=${searchFormData.item}`;

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
                        this.props.handle_result_change(response.data);
                    },
                    error => {
                        console.log(error);
                    }
                )
        }
    };

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
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
            <SecurityContext.Consumer>
                {(securityContext) => (
                    <Form onSubmit={e => this.handle_search(e, this.state)}>
                        <Form.Input
                            fluid
                            placeholder="Search by any attribute ..."
                            name="item"
                            value={this.state.item}
                            onChange={this.handle_change}
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

export default SearchByAnything;