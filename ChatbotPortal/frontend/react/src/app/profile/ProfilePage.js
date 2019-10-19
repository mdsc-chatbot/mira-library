import React from 'react';
import Profile from "./Profile";
import {SecurityContext} from '../security/SecurityContext';
import Nav from "../authentication/Nav";
import LoginForm from "../authentication/LoginForm";
import { Header, Icon, Divider, Table } from 'semantic-ui-react'

export default function ProfilePage() {
	return (
		<div>
			<Divider horizontal>
      			<Header as='h4'>
        		<Icon name='user' />
        		My Profile
      			</Header>
    		</Divider>

			<Divider horizontal>
      			<Header as='h4'>
        		View your profile below, edit feature coming soon.
      			</Header>
    		</Divider>

			<SecurityContext.Consumer>
				{(securityContext) => (
							<Table definition>
								{securityContext.security.logged_in ?
								<Table.Body>
									<Table.Row>
										<Table.Cell width={3}>Email</Table.Cell>
								  		<Table.Cell>{securityContext.security.email}</Table.Cell>
							  		</Table.Row>
							  		<Table.Row>
										<Table.Cell>First Name</Table.Cell>
								  		<Table.Cell>{securityContext.security.first_name}</Table.Cell>
							  		</Table.Row>
							  		<Table.Row>
								  		<Table.Cell>Last Name</Table.Cell>
								  		<Table.Cell>{securityContext.security.last_name}</Table.Cell>
							  		</Table.Row>
							  		<Table.Row>
								  		<Table.Cell>Status</Table.Cell>
								  		<Table.Cell>Newbie</Table.Cell>
							  		</Table.Row>
							  		<Table.Row>
								  		<Table.Cell>Submissions</Table.Cell>
								  		<Table.Cell>0</Table.Cell>
							  		</Table.Row>
							  		<Table.Row>
         						 		<Table.Cell>Points</Table.Cell>
								  		<Table.Cell>0</Table.Cell>
							  		</Table.Row>
								</Table.Body>
									: 'Nothing'}
							</Table>
					)}
			</SecurityContext.Consumer>
		</div>
	);
}