import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import {Dropdown} from 'semantic-ui-react';
import { SecurityContext } from "../security/SecurityContext";


export default class CategoryDropdown extends React.Component {
    static contextType = SecurityContext;

    static propTypes = {
        value : PropTypes.string,
        onChange : PropTypes.func.isRequired,
    };

    constructor(props) {
        super(props);

        this.state = {
            options : []
        }
    }

    componentDidMount() {
        // Fetch options for dropdown
        axios
            .get("/chatbotportal/resource/fetch-categories", {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            })
            .then(response => {
                this.setState({
                    options: response.data.map(category => ({
                        key: category.id,
                        value: category.id,
                        text: category.name
                    }))
                });
            });
    }

    handleChange = (event, data) => {
        this.props.onChange(data.value);
    };

    render() {
        return (
            <Dropdown
                fluid
                selection
                options={this.state.options}
                onChange={this.handleChange}
                value={this.props.value}
            />
        );
    };
}