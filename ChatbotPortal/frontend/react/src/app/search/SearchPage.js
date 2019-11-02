import React, {Component} from "react";
import SearchBar from "./SearchBar";
import SearchAdvancedOption from "./SearchAdvancedOption";
import {Header} from "semantic-ui-react";
import {SecurityContext} from "../security/SecurityContext";
import axios from "axios";

class SearchPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            total_users: ''
        }
    }

    static contextType = SecurityContext;

    componentDidMount() {
        this.get_total_user()
    }

    get_total_user = () => {
        const url = `http://127.0.0.1:8000/authentication/super/total/users/`;

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
                    console.log(response.data);
                    this.setState({

                        // Setting the response in user state
                        total_users: response.data['user_count'],
                    });
                },
                error => {
                    console.log(error);
                }
            )
    };

    render() {
        return (

            <div
                style={{paddingTop: 30, paddingLeft: 100, paddingRight: 100, height: 600}}
            >
                <Header
                    as="h3"
                    style={{
                        fontSize: "2em"
                    }}
                    color="blue"
                >
                    Search
                </Header>
                <SearchAdvancedOption />
                <SearchBar total_number_of_user = {this.state.total_users}/>
            </div>
        );
    }
}

export default SearchPage;
