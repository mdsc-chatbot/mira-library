	import React from 'react';
import Homepage from './Homepage';
import {Switch, Route} from "react-router-dom"
import {ProfilePage} from './profile';
import {ResourcePage} from './resource';
import {ReviewPage} from './review';
import HeaderMenu from './HeaderMenu';

export default function App(){
	return (
		<div>
			<HeaderMenu />
			<Switch>
				<Route path={baseRoute + '/profile'}>
					<ProfilePage />
				</Route>
				<Route path={baseRoute + '/resource'}>
					<ResourcePage />
				</Route>
				<Route path={baseRoute + '/review'}>
					<ReviewPage />
				</Route>
				<Route>
					<Homepage />
				</Route>
			</Switch>
		</div>
	)
}

export const baseRoute = '/chatbotportal/app';