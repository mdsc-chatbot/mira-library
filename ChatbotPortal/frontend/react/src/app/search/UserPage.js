import React, {Component} from 'react';
import axios from "axios";
import {SecurityContext} from '../contexts/SecurityContext';
import {
    Button,
    Card, CardContent, CardHeader,
    Checkbox,
    Container, Divider,
    Form, FormGroup,
    Icon,
    Image,
    Label,
    Responsive,
    Segment,
    SegmentGroup
} from 'semantic-ui-react';
import styles from "../profile/ProfilePage.css";

class UserPage extends Component {
    /**
     * This class renders the profile information
     * @type {React.Context<*>}
     */
    static contextType = SecurityContext;

    constructor(props) {
        /**
         * This constructor sets up the primary state for the props
         */
        super(props);
        this.state = {
            id: '',
            first_name: '',
            last_name: '',
            email: '',
            is_active: '',
            is_reviewer: '',
            is_staff: '',
            // profile_picture: ''

            horizontal_state: ''
        };
    };

    componentDidMount() {
        this.setState({
            first_name: this.props.rowData.first_name,
            last_name: this.props.rowData.last_name,
            affiliation: this.props.rowData.affiliation,

            //profile_picture: this.props.rowData.profile_picture

            is_active: this.props.rowData.is_active,
            is_reviewer: this.props.rowData.is_reviewer,
            is_staff: this.props.rowData.is_staff
        });

        if (window.innerWidth <= 760) {
            this.setState({
                horizontal_state: false
            });
        } else {
            this.setState({
                horizontal_state: true
            });
        }
    };

    /**
     * This function handles any changes that happens to the form fields
     * and store the changes to the state
     * @param e = event
     */
    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevState => {
            const newState = {...prevState};
            newState[name] = value;
            return newState;
        });
    };

    /**
     * This function handles the overall edit operations
     * @param e : event
     * @param editedData : data from the EditForm upon submission
     */
    handle_edit = (e, editedData) => {
        e.preventDefault();

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        /**
         * Perform a put request for edit.
         * Upon successful response, set the security context and component props with response data.
         * Otherwise, send an error is thrown."
         */
        axios
            .put(`/chatbotportal/authentication/super/${this.props.rowData.id}/update/`, editedData, {headers: options})
            .then(
                response => {
                    this.setState({
                        first_name: response.data['first_name'],
                        last_name: response.data['last_name'],

                    });
                },
                error => {
                    console.log(error);
                }
            );
    };

    /**
     * This function handles the delete operation
     * @param e : event
     */
    handle_delete = (e) => {
        e.preventDefault();

        // Defining header and content-type for accessing authenticated information
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        /**
         * Perform a delete request for deleting the user.
         * Upon successful response, returns 204 not found.
         * Otherwise, send an error is thrown."
         */
        axios
            .delete(`/chatbotportal/authentication/delete/${this.state.id}/`, {headers: options})
            .then(
                response => {
                    console.log(response.status)
                },
                error => {
                    console.log(error);
                }
            );

    };

    /**
     * This function handles the checkbox change options, and set the state accordingly
     * @param e : event
     * @param name : name of the checkbox field
     * @param value : value of the checkbox field
     */
    handle_toggle = (e, {name, value}) => {
        this.setState(prevState => {
            const newState = {...prevState};
            newState[name] = !value;
            return newState;
        });
    };

    set_mobile_format = () => {
        if (window.innerWidth <= 760) {
            this.setState({
                horizontal_state: false
            });
        } else {
            this.setState({
                horizontal_state: true
            });
        }
    };

    /**
     * This renders the ProfileForm
     * @returns {React.Fragment}
     */
    render() {
        return (
            <React.Fragment>
                <Responsive as={Container} minWidth={320} onUpdate={this.set_mobile_format}>
                    <Container>
                        <Form className={styles.centeredForm}>
                            <Segment className={styles.segmentBackground}>
                                <Label
                                    size='big'
                                    as='h1'
                                    icon='user'
                                    color='red'
                                    content={this.state.first_name ? `${this.state.first_name}'s Profile` : `${this.state.id}'s profile`}
                                    ribbon>
                                </Label>
                                <Card className={styles.cardBackground}
                                      fluid
                                      centered>
                                    {this.props.rowData.profile_picture ?
                                        <Image
                                            src={`/static/${this.props.rowData.profile_picture.split('/')[this.props.rowData.profile_picture.split('/').length - 1]}`}
                                            wrapped ui={true}/>
                                        : null}
                                    <CardContent>
                                        <CardHeader>
                                            <FormGroup widths='equal' unstackable>
                                                <Form.Input
                                                    className={styles.fixedInputHeight}
                                                    fluid
                                                    label='First name'
                                                    name='first_name'
                                                    onChange={this.handle_change}
                                                    value={this.state.first_name}/>
                                                <Form.Input
                                                    className={styles.fixedInputHeight}
                                                    fluid
                                                    label='Last name'
                                                    name='last_name'
                                                    onChange={this.handle_change}
                                                    value={this.state.last_name}/>
                                            </FormGroup>
                                        </CardHeader>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='id badge'/>
                                            {this.props.rowData.id}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='mail'/>
                                            {this.props.rowData.email}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='dropbox'/>
                                            Submissions: {this.props.rowData.submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='thumbs up'/>
                                            Reviewed: {this.props.rowData.approved_submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='wait'/>
                                            Pending: {this.props.rowData.pending_submissions}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='trophy'/>
                                            Points: {this.props.rowData.points}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3><Icon color='red' name='heart'/>
                                        Affiliation: </h3> {this.props.rowData.affiliation}
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='sign in'/>
                                            Last logged: {this.props.rowData.last_login}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <h3>
                                            <Icon color='red' name='registered'/>
                                            Registered on: {this.props.rowData.date_joined}
                                        </h3>
                                    </CardContent>
                                    <CardContent extra>
                                        <SegmentGroup horizontal={this.state.horizontal_state}>
                                            <Segment color='red'>
                                                <Checkbox
                                                    checked={this.state.is_active}
                                                    label='Active'
                                                    name='is_active'
                                                    value={this.state.is_active}
                                                    onChange={this.handle_toggle}
                                                    slider
                                                />
                                            </Segment>
                                            <Segment color='red'>
                                                <Checkbox
                                                    checked={this.state.is_reviewer}
                                                    label='Reviewer'
                                                    name='is_reviewer'
                                                    value={this.state.is_reviewer}
                                                    onChange={this.handle_toggle}
                                                    slider
                                                />
                                            </Segment>
                                            <Segment color='red'>
                                                <Checkbox
                                                    checked={this.state.is_staff}
                                                    label='Staff'
                                                    name='is_staff'
                                                    value={this.state.is_staff}
                                                    onChange={this.handle_toggle}
                                                    slider
                                                />
                                            </Segment>
                                        </SegmentGroup>

                                        <SegmentGroup horizontal={this.state.horizontal_state} size={"mini"}>
                                            <Segment>
                                                <Button
                                                    color='green'
                                                    fluid
                                                    size='small'
                                                    onClick={e => this.handle_edit(e, this.state)}>
                                                    <Icon name='save'/>Save
                                                </Button>
                                            </Segment>
                                            <Segment>
                                                <Button
                                                    color='red'
                                                    fluid
                                                    size='small'
                                                    onClick={e => this.handle_delete(e)}>
                                                    <Icon name='delete'/>Delete
                                                </Button>
                                            </Segment>
                                        </SegmentGroup>
                                    </CardContent>
                                </Card>
                            </Segment>
                        </Form>
                    </Container>
                </Responsive>
            </React.Fragment>
        );
    }
}

export default UserPage;
