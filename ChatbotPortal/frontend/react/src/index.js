/**
 * @file: index.js
 * @summary: App index
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
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