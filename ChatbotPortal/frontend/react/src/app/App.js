// import React from 'react';
// import Homepage from './Homepage';
// import {Switch, Route} from "react-router-dom"
// import {ProfilePage} from './profile';
// import {ResourcePage} from './resource';
// import {ReviewPage} from './review';
// import HeaderMenu from './HeaderMenu';

// export default function App(){
// 	return (
// 		<div>
// 			<HeaderMenu />
// 			<Switch>
// 				<Route path={baseRoute + '/profile'}>
// 					<ProfilePage />
// 				</Route>
// 				<Route path={baseRoute + '/resource'}>
// 					<ResourcePage />
// 				</Route>
// 				<Route path={baseRoute + '/review'}>
// 					<ReviewPage />
// 				</Route>
// 				<Route>
// 					<Homepage />
// 				</Route>
// 			</Switch>
// 		</div>
// 	)
// }
//
// export const baseRoute = '/chatbotportal/app';

import React, { Component } from 'react';
import Nav from './authentication/Nav';
import LoginForm from './authentication/LoginForm';
import SignupForm from './authentication/SignupForm';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      email: '',
      first_name: ''
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
          this.setState({ email: json.email });
        });
    }
  }

  handle_login = (e, data) => {
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
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          email: json.user.email
        });
      });
  };

  handle_signup = (e, data) => {
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
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          email: json.email,
          first_name: json.first_name,
          last_name: json.last_name,
          affiliation: json.affiliation
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, email: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="App">
        <Nav
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3>
          {this.state.logged_in
            ? `Hello, ${this.state.first_name}`
            : 'Please Log In'}
        </h3>
      </div>
    );
  }
}

export default App;