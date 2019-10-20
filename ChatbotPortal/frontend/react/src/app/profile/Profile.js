import React from 'react'
function Profile() {

	const users = ['Ritvik','Khanna','ritvik@ualberta.ca']

	return (
		<React.Fragment>
			{users.map( user=> {
				return <h3>{user}</h3>
				})}
		</React.Fragment>
	)

}

export default Profile;