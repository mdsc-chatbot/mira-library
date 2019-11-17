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
            <Route>
                <PublicResourcesView />
            </Route>
        </Switch>
    );
}

PublicResourcePage.propTypes = {
    match : PropTypes.object,
};

export default PublicResourcePage;
