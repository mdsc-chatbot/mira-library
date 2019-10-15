import React from 'react';
import {Link} from 'react-router-dom';
import {baseRoute} from './App';

export default function HeaderMenu() {
	const linkstyle = {
		color: "white",
		backgroundColor: "DodgerBlue",
		padding: "10px",
	};

	return (
		<span>
			<Link to={baseRoute}><div style={linkstyle}>Home</div></Link>
			<Link to={baseRoute + "/profile"}><div style={linkstyle}>Profile</div></Link>
			<Link to={baseRoute + "/resource"}><div style={linkstyle}>Resource</div></Link>
			<Link to={baseRoute + "/review"}><div style={linkstyle}>Review</div></Link>
		</span>
	);
}