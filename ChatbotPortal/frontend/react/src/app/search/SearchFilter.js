import React from "react";
import { Button, Dropdown, Form, Grid, Checkbox } from "semantic-ui-react";
import axios from "axios";
import { SecurityContext } from "../security/SecurityContext";

const filter_by = [
    { key: "is_active", value: "is_active", text: "Is active?" },
    { key: "is_reviewer", value: "is_reviewer", text: "Is a reviewer?" },
    { key: "is_staff", value: "is_staff", text: "Is a staff?" },
    { key: "is_superuser", value: "is_superuser", text: "Is a superuser?" }
];

const filter_value = [
    { key: "true", value: "True", text: "Yes" },
    { key: "false", value: "False", text: "No" }
];

/**
 * This class helps filtering users based on either is_active or is_reviewer or is_staff or is_superuser
 */
class SearchFilter extends React.Component {
    static contextType = SecurityContext;

    /**
     * This is the constructor that declare the initial state with default values.
     * @param props = Properties that will be used in the constructor
     */
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{is_logged_in: boolean, filterValue: string, filterBy: string}}
         */
        this.state = {
            is_logged_in: false,
            filterBy: "is_active",
            filterValue: "True"
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
        if (
            this.state.is_logged_in === false &&
            this.context.security &&
            this.context.security.is_logged_in
        ) {
            this.setState({
                is_logged_in: this.context.security.is_logged_in
            });
        }
    };

    /**
     * This function executes the query by calling backend controller (API),
     * which returns the filtered users.
     * @param e = event
     * @param searchFormData = Data received from search form
     */
    handle_search = (e, searchFormData) => {
        // prevent the browser to reload itself (Ask Henry if it is necessary)
        e.preventDefault();
        if (this.context.security.is_logged_in) {
            // The backend URL
            const url = `http://127.0.0.1:8000/authentication/super/search/filter/${searchFormData.filterBy}/${searchFormData.filterValue}/`;

            // Having the permission header loaded
            const options = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.context.security.token}`
            };

            /**
             * Calling the backend API
             */
            axios.get(url, { headers: options }).then(
                response => {
                    this.setState({
                        // Setting the response in user state
                        users: response.data
                    });
                },
                error => {
                    console.log(error);
                }
            );
        }
    };

    /**
     * This function handles the changes that happen to the state in the drop down field of the form.
     * @param e = Event
     * @param value = The value from the drop down form that will be stored in the state
     * @param key = Key of the value-
     */
    handle_change_dropdown = (value, key) => {
        this.setState({ [key]: value });
    };

    /**
     * This function renders the form containing the Dropdown options
     * @returns {*}
     */
    render() {
        return (
            <SecurityContext.Consumer>
                {securityContext => (
                    <div>
                        <Checkbox
                            label="User"
                            onChange={this.toggle}
                            checked={this.state.checked_user}
                            style={{ paddingLeft: 20 }}
                        />
                        <Checkbox
                            label="Review"
                            onChange={this.toggle}
                            checked={this.state.checked_review}
                            style={{ paddingLeft: 20 }}
                        />
                        <Checkbox
                            label="Admin"
                            onChange={this.toggle}
                            checked={this.state.checked_admin}
                            style={{ paddingLeft: 20 }}
                        />
                        <Checkbox
                            label="Active"
                            onChange={this.toggle}
                            checked={this.state.checked_active}
                            style={{ paddingLeft: 20 }}
                        />
                    </div>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default SearchFilter;
