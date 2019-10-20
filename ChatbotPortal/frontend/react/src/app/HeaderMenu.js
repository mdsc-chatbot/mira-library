import React from 'react';
import {Link} from 'react-router-dom';
import {Menu, Label, Image} from 'semantic-ui-react';
import {baseRoute} from './App';

export default function HeaderMenu() {

	return (
		<Menu color = 'green'>
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

			<Menu.Menu position='right'>
          		<Menu.Item>
					 <Label as='a' color='blue' image>
     					 <Image size='tiny' src='https://www.iconsdb.com/icons/download/color/4AFFFF/checked-user-24.png' />
     					  My Self
    					</Label>
					<Link to={baseRoute + "/profile"}/>
          		</Menu.Item>
			</Menu.Menu>

		</Menu>
	);
}