import React, {Component} from "react";
import SearchTable from "./SearchTable";
import SearchAdvancedOption from "./SearchAdvancedOption";
import {Button, Header} from "semantic-ui-react";
import SearchByAnything from "./SearchByAnything";

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
            submission_range_option: '',

            search_string: '',

            url: "http://127.0.0.1:8000/authentication/super/search/status/''/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search="
        };
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
        console.log(this.state)
        e.preventDefault();
        this.setState({
            search_clicked: true,
            url: `http://127.0.0.1:8000/authentication/super/search/status/${this.state.is_active}/${this.state.is_reviewer}/${this.state.is_staff}/${this.state.is_superuser}/date_range/${this.state.search_option}/${this.state.start_date}/${this.state.end_date}/id_range/${this.state.start_id}/${this.state.end_id}/submission_range/${this.state.start_submission}/${this.state.end_submission}/${this.state.submission_range_option}/search_value/?search=${this.state.search_string}`
        });
    };

    /**
     * This renders the search related components
     * @returns {*}
     */
    render() {
        return (
            <div
                style={{paddingTop: 30, paddingLeft: 100, paddingRight: 100, minHeight: 600}}
            >
                <Header
                    as="h3"
                    style={{
                        fontSize: "2em"
                    }}
                    color="blue"
                >
                    Search
                </Header>
                <SearchByAnything set_search_string={this.set_search_string}/>
                <SearchAdvancedOption set_date_range_params={this.set_date_range_params}
                                      set_date_option_params={this.set_date_option_params}
                                      set_status_search_params={this.set_status_search_params}
                                      set_id_search_params={this.set_id_search_params}
                                      set_submission_search_params={this.set_submission_search_params}/>
                <Button
                    color="blue"
                    fluid size="large"
                    onClick={this.submit_query}
                >Search
                </Button>
                <SearchTable url={this.state.url} search_clicked={this.state.search_clicked}/>
            </div>
        );
    }
}

export default SearchPage;
