import React from 'react';
import Profile from "./Profile";
import {SecurityContext} from '../security/SecurityContext';
import Nav from "../authentication/Nav";
import LoginForm from "../authentication/LoginForm";
import { Header, Icon, Divider, Table, Message, Container, Input } from 'semantic-ui-react'
import Image from "semantic-ui-react/dist/commonjs/elements/Image";
import {unstable_renderSubtreeIntoContainer} from "react-dom";
// import styles from './ProfilePage.css'

export default function ProfilePage() {
	return (

		<Container>
			<div>
				<Divider horizontal>
					<Header as='h4'>
						<Icon name='user' />
						My Profile
					</Header>
				</Divider>

				<SecurityContext.Consumer>
					{(securityContext) => (
						<div>
							<Table definition color='blue'>
								{securityContext.security.logged_in ?
									<Table.Body>
										<Table.Row>
											<Table.Cell width={3}>Profile Picture</Table.Cell>
											<Table.Cell>
												<Image src='https://www.iconsdb.com/icons/download/color/4AFFFF/user-512.png' size='small' />
											</Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell>Email</Table.Cell>
											<Table.Cell>
												<Input defaultValue={securityContext.security.email} />
											</Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell>First Name</Table.Cell>
											<Table.Cell><Input  defaultValue={securityContext.security.first_name} /></Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell >Last Name</Table.Cell>
											<Table.Cell><Input defaultValue={securityContext.security.last_name} />
											</Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell>Status</Table.Cell>
											<Table.Cell>Newbie</Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell>Submissions</Table.Cell>
											<Table.Cell >0</Table.Cell>
										</Table.Row>
										<Table.Row>
											<Table.Cell>Points</Table.Cell>
											<Table.Cell >0</Table.Cell>
										</Table.Row>
									</Table.Body>
									:
									<Message icon error>
										<Icon name='circle notched' loading/>
										<Message.Content>
											<Message.Header>Nothing to show here!</Message.Header>
											Log in and try again?
										</Message.Content>
									</Message>}
							</Table>
						</div>

					)}
				</SecurityContext.Consumer>
			</div>
		</Container>

	);
}