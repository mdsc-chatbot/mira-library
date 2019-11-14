import React from "react";
import {Dropdown} from "semantic-ui-react";

const options = [
    {key: 1, text: 'Yes', value: true},
    {key: 2, text: 'No', value: false},
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
            <div>
                <div style={{float:"left", paddingRight:20}}>
                    <p>Active</p>
                    <Dropdown
                        clearable
                        name='is_active'
                        onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                        options={options}
                        placeholder='None'
                        selection
                    >
                    </Dropdown>
                </div>
                <div style={{ float: "left", paddingRight:20}}>
                    <p>Reviewer</p>
                    <Dropdown
                        clearable
                        name='is_reviewer'
                        onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                        options={options}
                        placeholder='None'
                        selection
                    >
                    </Dropdown>
                </div>
                <div>
                    <p>Staff</p>
                    <Dropdown
                        clearable
                        name='is_staff'
                        onChange={(e, {name, value}) => this.handle_change_dropdown({name, value})}
                        options={options}
                        placeholder='None'
                        selection
                    >
                    </Dropdown>
                </div>
            </div>
        );
    }
}

export default SearchFilter;
