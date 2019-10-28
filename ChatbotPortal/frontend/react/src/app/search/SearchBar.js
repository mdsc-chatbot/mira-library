import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";
import {Table} from "semantic-ui-react";

class SearchBar extends Component {
    static contextType = SecurityContext;

    BASE_URL = 'http://127.0.0.1:8000/authentication/';

    constructor(props) {
        super(props);
        this.state = {
            users: {}
        }
    }

    componentDidMount() {
        this.get_users();
    }

    get_users = () => {
        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(this.BASE_URL + 'super/search/alluser/', {headers : options})
            .then(
                response => {
                    console.log(response.data)
                    this.setState({
                        users : response.data,
                    });
                },
                error => {
                    console.log(error);
                }
            )
    };


    get_data = () =>{
        return(
            this.state.users.length > 0 && this.state.users.map(user => (
                <tr>
                    <td>{user.id}</td>
                    <td>{user.first_name}</td>
                    <td>{user.last_name}</td>
                    <td>{user.email}</td>
                    <td>{user.date_joined}</td>
                    <td>{user.last_login}</td>
                    <td>{user.is_active.toString()}</td>
                    <td>{user.is_reviewer.toString()}</td>
                    <td>{user.is_staff.toString()}</td>
                    <td>{user.is_superuser.toString()}</td>
                    <td>{user.affiliation}</td>
                </tr>
            ))
        )
    }

    render() {
        return(
            <div>
                <div style={styles.outside_table}>
                    Users
                    {/*<button className="ui right floated button"*/}
                    {/*        onClick={() => this.switchView()}>{this.state.pending}</button>*/}
                    <div style={styles.inside_table}>
                    <Table class="ui celled table">
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Email</th>
                            <th>Created on</th>
                            <th>Last Logged</th>
                            <th>Is Active</th>
                            <th>Is Reviewer</th>
                            <th>Is Staff</th>
                            <th>Is Superuser</th>
                            <th>Affiliation</th>
                        </tr>
                        </thead>
                        <tbody>
                        {this.context.security.is_logged_in ?
                            (this.get_data()) : null}
                        </tbody>
                    </Table>
                    </div>
                </div>
            </div>
        );
    }
}

export default SearchBar;

const styles = {
    outside_table: {
        paddingTop: 30,
        paddingLeft: 100,
        paddingRight: 100
    }
};