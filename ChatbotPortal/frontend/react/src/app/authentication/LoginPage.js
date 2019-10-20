import React, {Component} from 'react';
import Nav from './Nav';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import {SecurityContext} from '../security/SecurityContext';

// import './App.css';

class LoginPage extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            displayed_form: 'login',
            id: '',
            email: '',
            first_name: '',
            last_name: '',
            affiliation: '',
            active: '',
            staff: '',
            admin: ''
        };
    }

    componentDidMount() {
        if (this.context.security.logged_in) {
            fetch('http://localhost:8000/signup/current_user/', {
                headers: {
                    Authorization: `JWT ${this.context.security.token}`
                }
            })
                .then(res => res.json())
                .then(json => {
                    this.setState({
                        id: json.id,
                        email: json.email,
                        first_name: json.first_name,
                        last_name: json.last_name
                    });
                });
        }
    }

    handle_login = (e, data, setSecurity) => {
        e.preventDefault();
        fetch('http://localhost:8000/token-auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(json => {

                setSecurity({
                    token: json.token,
                    logged_in: true,
                    id: json.user.id,
                    email: json.user.email,
                    first_name: json.user.first_name,
                    last_name: json.user.last_name,
                    affiliation: json.user.affiliation,
                    active: json.user.active,
                    staff: json.user.staff,
                    admin: json.user.admin,
                });
                this.setState({
                    displayed_form: '',
                });
            });
    };

    handle_signup = (e, data, setSecurity) => {
        e.preventDefault();
        fetch('http://localhost:8000/signup/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(json => {
                setSecurity({
                    token: json.token,
                    logged_in: true,
                    id: json.id,
                    email: json.email,
                    first_name: json.first_name,
                    last_name: json.last_name,
                    affiliation: json.affiliation
                });
                this.setState({
                    displayed_form: '',
                });
            });
    };

    handle_logout = () => {
        this.context.setSecurity({
            logged_in : false
        });
    };

    display_form = form => {
        this.setState({
            displayed_form: form
        });
    };

    set_form_to_signup = () => {
        this.display_form('signup');
    };

    render() {
        return (

            <SecurityContext.Consumer>
                {(securityContext) => (
                    <div className="App">
                        <Nav
                            logged_in={this.context.security.logged_in}
                            display_form={this.display_form}
                            handle_logout={this.handle_logout}
                        />
                        {
                            this.state.displayed_form === 'login' ? (
                                <LoginForm
                                    handle_login={(event, data) => this.handle_login(event, data, securityContext.setSecurity)}
                                    handleRegisterClicked={this.set_form_to_signup}
                                />
                            ) : this.state.displayed_form === 'signup' ? (
                                <SignupForm
                                    handle_signup={(event, data) => this.handle_signup(event, data, securityContext.setSecurity)}
                                />
                            ) : null
                        }
                        <h3>
                            {securityContext.security.logged_in
                                ? `Hello, ${securityContext.security.id}`
                                : 'Please Log In'}
                        </h3>
                    </div>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default LoginPage;