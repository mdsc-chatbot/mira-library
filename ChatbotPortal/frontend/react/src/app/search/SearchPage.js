import React, {Component} from "react";
import {
    Button,
    Checkbox,
    Container,
    Form,
    FormGroup,
    Header,
    Responsive,
    Segment,
    Sidebar,
    SidebarPushable,
    SidebarPusher
} from "semantic-ui-react";
import {SecurityContext} from "../contexts/SecurityContext";
import SearchByAnything from "./SearchByAnything";
import SearchAdvancedOption from "./SearchAdvancedOption";
import SearchTable from "./SearchTable";
import styles from "./SearchPage.css"

class SearchPage extends Component {

    /**
     * This constructor initializes the state that is required for the search app.
     * @param props = Properties passed down from the parent component
     */
    constructor(props) {
        super(props);

        /**
         * This is the state of this component.
         * @type {{end_date: string, start_submission: string, is_active: string, is_superuser: string, is_reviewer: string, is_staff: string, start_id: string, end_id: string, loadedData: [], search_string: string, url: string, search_option: string, end_submission: string, search_clicked: boolean, start_date: string}}
         */
        this.state = {
            search_clicked: false,
            loadedData: [],

            is_active: "''",
            is_reviewer: "''",
            is_staff: "''",
            is_superuser: "''",

            search_option: "''",
            start_date: "''",
            end_date: "''",

            start_id: "''",
            end_id: "''",

            start_submission: "''",
            end_submission: "''",
            submission_range_option: "''",

            search_string: '',

            url: "/chatbotportal/authentication/super/search/status/''/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search=",

            sidebar_visible: true,
            checkbox_visible: false,
            width: "thin",
            animation: "slide out"
        };
    }

    componentDidMount() {
        this.set_sidebar_visibility();
    }

    /**
     * Gets called when the state gets changed.
     * @param prevProps
     * @param prevState
     * @param snapshot
     */
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.state.search_clicked) {
            this.setState({
                search_clicked: false
            });
        }
    }

    /**
     * This function sets the date range state and will be passed to the SearchByDateRange component
     * @param start_date
     * @param end_date
     */
    set_date_range_params = (start_date, end_date) => {
        this.setState({
            start_date: start_date,
            end_date: end_date
        })
    };

    /**
     * This function sets the date option state and will be passed to the SearchByDateRange component
     * @param search_option
     */
    set_date_option_params = (search_option) => {
        this.setState({
            search_option: search_option
        })
    };

    /**
     * This function sets the status filter and will be passed to the SearchFilter component
     * @param name
     * @param value
     */
    set_status_search_params = ({name, value}) => {
        this.setState({[name]: value});
    };

    /**
     * This function sets the id range state and will be passed to the SearchByIdRange component
     * @param name
     * @param value
     */
    set_id_search_params = ({name, value}) => {
        this.setState({[name]: value});
    };

    /**
     * This function sets the submission range state and will be passed to the SearchBySubmissionRange component
     * @param name
     * @param value
     */
    set_submission_search_params = ({name, value}) => {
        this.setState({[name]: value});
    };

    /**
     * This function sets the search string state and will be passed to the SearchByAnything component
     * @param name
     * @param value
     */
    set_search_string = ({name, value}) => {
        this.setState({[name]: value});
    };

    /**
     * This function generates the query URL after clicking Search button
     * @param e = event
     */
    submit_query = (e) => {
        console.log(this.state);
        e.preventDefault();
        this.setState({
            search_clicked: true,
            url: `/chatbotportal/authentication/super/search/status/${this.state.is_active}/${this.state.is_reviewer}/${this.state.is_staff}/${this.state.is_superuser}/date_range/${this.state.search_option}/${this.state.start_date}/${this.state.end_date}/id_range/${this.state.start_id}/${this.state.end_id}/submission_range/${this.state.start_submission}/${this.state.end_submission}/${this.state.submission_range_option}/search_value/?search=${this.state.search_string}`
        });
    };

    set_sidebar_visibility = () => {
        if (window.innerWidth <= 760) {
            this.setState({
                sidebar_visible: false,
                checkbox_visible: true,
                width: "wide",
                animation: "scale down"
            })
        } else {
            this.setState({
                sidebar_visible: true,
                checkbox_visible: false,
                width: "thin",
                animation: "slide out"
            })
        }

    };

    handle_toggle = (e, {name, value}) => {
        this.setState(prevState => {
            const newState = {...prevState};
            newState[name] = !value;
            return newState;
        });
    };

    /**
     * This renders the search related components
     * @returns {*}
     */
    render() {
        return (
            <SecurityContext.Consumer>
                {(securityContext) => (
                    <Responsive as={SidebarPushable} minWidth={320} onUpdate={this.set_sidebar_visibility}>
                        {securityContext.security.is_logged_in ?
                            <SidebarPushable as={Segment}>
                                <Sidebar
                                    className={styles.sidebarStyle}
                                    as={Container}
                                    animation={this.state.animation}
                                    icon='labeled'
                                    inverted
                                    vertical
                                    visible={this.state.sidebar_visible}
                                    width={this.state.width}>
                                    <Responsive as={Container} minWidth={320}>
                                        <Container
                                            className={styles.advancedSearchView}
                                            fluid>
                                            <SearchAdvancedOption
                                                set_date_range_params={this.set_date_range_params}
                                                set_date_option_params={this.set_date_option_params}
                                                set_status_search_params={this.set_status_search_params}
                                                set_id_search_params={this.set_id_search_params}
                                                set_submission_search_params={this.set_submission_search_params}/>
                                        </Container>
                                    </Responsive>
                                </Sidebar>
                                <Responsive as={SidebarPusher} minWidth={320}>
                                    <SidebarPusher>
                                        <Segment basic>
                                            {this.state.checkbox_visible ?
                                                <Checkbox
                                                    className={styles.checkboxStyle}
                                                    checked={this.state.sidebar_visible}
                                                    name='sidebar_visible'
                                                    value={this.state.sidebar_visible}
                                                    onChange={this.handle_toggle}
                                                    slider/>
                                                : null}
                                            <Responsive as={Header} minWidth={320}>
                                                <Header
                                                    as="h1"
                                                    className={styles.headerStyle}
                                                    color="blue"
                                                    content="Search"/>
                                            </Responsive>
                                            <Responsive as={Form} minWidth={320}>
                                                <Form size="mini">
                                                    <FormGroup>
                                                        <Button
                                                            id="search_button"
                                                            icon="search"
                                                            color="blue"
                                                            size="mini"
                                                            onClick={this.submit_query}/>
                                                        < SearchByAnything set_search_string={this.set_search_string}/>
                                                    </FormGroup>
                                                </Form>
                                            </Responsive>
                                        </Segment>
                                        <Container
                                            className={styles.searchTableView}
                                            fluid>
                                            <SearchTable
                                                url={this.state.url}
                                                search_clicked={this.state.search_clicked}/>
                                        </Container>
                                    </SidebarPusher>
                                </Responsive>
                            </SidebarPushable>
                            : null}
                    </Responsive>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default SearchPage;
