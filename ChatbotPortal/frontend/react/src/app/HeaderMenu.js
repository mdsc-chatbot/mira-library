import React from 'react';
import {Link} from 'react-router-dom';
import {Menu} from 'semantic-ui-react';
import {baseRoute} from './App';

export default function HeaderMenu() {

	return (
		<Menu>
			<Menu.Item name='home'>
				<Link to={baseRoute}>Home</Link>
			</Menu.Item>
			<Menu.Item name='profile'>
				<Link to={baseRoute + "/profile"}>Profile</Link>
			</Menu.Item>
			<Menu.Item name='resource'>
				<Link to={baseRoute + "/resource"}>Resource</Link>
			</Menu.Item>
			<Menu.Item name='review'>
				<Link to={baseRoute + "/review"}>Review</Link>
			</Menu.Item>
			<Menu.Item name='login'>
				<Link to={baseRoute + "/login"}>Login</Link>
			</Menu.Item>
		</Menu>
	);
}