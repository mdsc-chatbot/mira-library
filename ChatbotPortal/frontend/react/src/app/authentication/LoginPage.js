import React, {Component} from 'react';
import Nav from './Nav';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import {SecurityContext} from '../security/SecurityContext';

// import './App.css';

class LoginPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            displayed_form: 'login',
            logged_in: localStorage.getItem('token') ? true : false,
            email: '',
            first_name: '',
            last_name: '',
            affiliation: '',
            active: '',
            staff: '',
            admin: '',
        };
    }

    componentDidMount() {
        if (this.state.logged_in) {
            fetch('http://localhost:8000/signup/current_user/', {
                headers: {
                    Authorization: `JWT ${localStorage.getItem('token')}`
                }
            })
                .then(res => res.json())
                .then(json => {
                    this.setState({email: json.email});
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
                    email: json.user.email,
                    first_name: json.user.first_name,
                    last_name: json.user.last_name,
                    affiliation: json.user.affiliation,
                    active: json.user.active,
                    staff: json.user.staff,
                    admin: json.user.admin,
                });
                localStorage.setItem('token', json.token);
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
        localStorage.removeItem('token');
        this.setState({logged_in: false, email: ''});
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
        let form;
        switch (this.state.displayed_form) {
            case 'login':
                form = <LoginForm handle_login={this.handle_login}/>;
                break;
            case 'signup':
                form = <SignupForm handle_signup={this.handle_signup}/>;
                break;
            default:
                form = null;
        }

        return (

            <SecurityContext.Consumer>
                {(securityContext) => (
                    <div className="App">
                        <Nav
                            logged_in={this.state.logged_in}
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
                                ? `Hello, ${securityContext.security.email}`
                                : 'Please Log In'}
                        </h3>
                    </div>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default LoginPage;