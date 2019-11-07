import React from "react";
import {Checkbox} from "semantic-ui-react";

/**
 * This class helps filtering users based on either is_active or is_reviewer or is_staff or is_superuser
 */
class SearchFilter extends React.Component {
    constructor(props) {
        super(props);

        /**
         * The state of this component
         * @type {{is_logged_in: boolean, filterValue: string, filterBy: string}}
         */
        this.state = {
            is_active: false,
            is_reviewer: false,
            is_staff: false,
            is_superuser: false
        };
    }

    handle_toggle = (e, {name, value}) => {
        this.setState(prevState => {
            const newState = {...prevState};
            newState[name] = !value;
            return newState;
        });
        this.props.set_status_search_params({name, value});
    };

    /**
     * This function renders the form containing the Dropdown options
     * @returns {*}
     */
    render() {
        return (

            <div>
                <Checkbox
                    checked={this.state.is_active}
                    label='Active'
                    name='is_active'
                    value={this.state.is_active}
                    onChange={this.handle_toggle}
                    style={{paddingLeft: 20}}
                />
                <Checkbox
                    checked={this.state.is_reviewer}
                    label='Reviewer'
                    name='is_reviewer'
                    value={this.state.is_reviewer}
                    onChange={this.handle_toggle}
                    style={{paddingLeft: 20}}
                />
                <Checkbox
                    checked={this.state.is_staff}
                    label='Staff'
                    name='is_staff'
                    value={this.state.is_staff}
                    onChange={this.handle_toggle}
                    style={{paddingLeft: 20}}
                />
                <Checkbox
                    checked={this.state.is_superuser}
                    label='Superuser'
                    name='is_superuser'
                    value={this.state.is_superuser}
                    onChange={this.handle_toggle}
                    style={{paddingLeft: 20}}
                />
            </div>
        );
    }
}

export default SearchFilter;
