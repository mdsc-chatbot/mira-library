import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Route} from 'react-router-dom';
import axios from 'axios';
import {default as App} from './app/App';
import 'semantic-ui-less/semantic.less';

// Axios setup
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

if (document.getElementById('root') !== null) {
    ReactDOM.render(
        <BrowserRouter baseName={'/chatbotportal/app'}>
            <Route path="*" component={App} />
        </BrowserRouter>,
        document.getElementById('root')
    );
}