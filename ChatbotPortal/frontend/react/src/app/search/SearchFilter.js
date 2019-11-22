import React from "react";
import {Form, Container, Dropdown, Responsive} from "semantic-ui-react";

const options = [
    {key: 1, text: 'Yes', value: 'true'},
    {key: 2, text: 'No', value: 'false'},
    {key: 3, text: 'None', value: "''"},
];

/**
 * This class helps filtering users based on either is_active or is_reviewer or is_staff
 */
class SearchFilter extends React.Component {

    /**
     * This function handles the changes in the drop down and alters the parent props
     * @param name = name of the drop down
     * @param value = value from the options
     */
    handle_change_dropdown = ({name, value}) => {
        if (!!value) {
            this.props.set_status_search_params({name, value});
        } else {
            value = "''";
            this.props.set_status_search_params({name, value});
        }
    };

    /**
     * This function renders the form containing the Dropdown options
     * @returns {*}
     */
    render() {
        return (
            <Form size='mini'>
                <Container content='Active'/>
                <Dropdown
                    name='is_active'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
                <Container content='Reviewer'/>
                <Dropdown
                    name='is_reviewer'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
                <Container content='Staff'/>
                <Dropdown
                    name='is_staff'
                    onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                    options={options}
                    placeholder='None'
                    selection
                />
            </Form>
        );
    }
}

export default SearchFilter;
