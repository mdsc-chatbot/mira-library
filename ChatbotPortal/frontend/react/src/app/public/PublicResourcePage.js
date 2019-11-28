/**
 * @file: PublicResourcePage.js
 * @summary: Routing for detail public resource view and list of public resources
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

import React, { Component } from "react";
import PropTypes from 'prop-types';
import {Switch, Route} from 'react-router';
import PublicResourcesView from './PublicResourcesView';
import DetailedPublicResource from './DetailedPublicResource';

export function PublicResourcePage({match}) {

    return (
        <Switch>
            <Route path={`${match.path}/detail/:id`}>
                {({match}) => (
                    <DetailedPublicResource resourceId={match.params.id} />
                )}
            </Route>
            <Route path={`${match.path}/:tagid`}>
                {({match}) => (
                    <PublicResourcesView tagId={match.params.tagid}/>
                )}
            </Route>
            <Route >
                <PublicResourcesView />
            </Route>
        </Switch>
    );
}

PublicResourcePage.propTypes = {
    match : PropTypes.object,
};

export default PublicResourcePage;
