import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";
import {Table, Column} from 'react-virtualized';
import 'react-virtualized/styles.css';

// const {Table, Column} = ReactVirtualized;

class SearchBar extends Component {
    static contextType = SecurityContext;

    BASE_URL = 'http://127.0.0.1:8000/authentication/';

    constructor(props) {
        super(props);
        this.state = {
            users: ''
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
                    console.log(response.data);
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
    };

    render() {
        return(
            <div className="container">
                <h1>Table example </h1>
                <Table
                    rowClassName='table-row'
                    headerHeight={40}
                    width={600}
                    height={300}
                    rowHeight={40}
                    rowCount={this.state.users.length}
                    rowGetter={({index}) => this.state.users[index]}
                >
                    <Column
                        label='Id'
                        dataKey='id'
                        width={50}
                    />
                    <Column
                        label='E.mail'
                        dataKey='email'
                        width={300}
                    />
                </Table>
            </div>
        );
    }
}

export default SearchBar;
