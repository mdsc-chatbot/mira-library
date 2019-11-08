import React, {Component} from "react";
import SearchTable from "./SearchTable";
import SearchAdvancedOption from "./SearchAdvancedOption";
import {Button, Header} from "semantic-ui-react";
import {SecurityContext} from "../security/SecurityContext";
import SearchByAnything from "./SearchByAnything";

class SearchPage extends Component {
    constructor(props) {
        super(props);
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

            search_string: '',

            url: "http://127.0.0.1:8000/authentication/super/search/status/''/''/''/''/date_range/''/''/''/id_range/''/''/search_value/?search="
        };
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        console.log("In the searchPage Update.");
        if (this.state.search_clicked) {
            this.setState({
                search_clicked: false
            });
        }
    }

    set_date_range_params = (start_date, end_date) => {
        this.setState({
            start_date: start_date,
            end_date: end_date
        })
    };

    set_date_option_params = (search_option) => {
        this.setState({
            search_option: search_option
        })
    };

    set_status_search_params = ({name, value}) => {
        this.setState({[name]: !value});
    };

    set_id_search_params = ({name, value}) => {
        this.setState({[name]: value});
    };

    set_search_string = ({name, value}) => {
        this.setState({[name]: value});
    };

    submit_query = (e) => {
        e.preventDefault();
        this.setState({
            search_clicked: true,
            url: `http://127.0.0.1:8000/authentication/super/search/status/${this.state.is_active}/${this.state.is_reviewer}/${this.state.is_staff}/${this.state.is_superuser}/date_range/${this.state.search_option}/${this.state.start_date}/${this.state.end_date}/id_range/${this.state.start_id}/${this.state.end_id}/search_value/?search=${this.state.search_string}`
        });
    };

    static contextType = SecurityContext;

    render() {
        return (

            <div
                style={{paddingTop: 30, paddingLeft: 100, paddingRight: 100, height: 600}}
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
                                      set_id_search_params={this.set_id_search_params}/>
                <Button color="blue" fluid size="large" onClick={this.submit_query}>Search</Button>
                <SearchTable url={this.state.url} search_clicked={this.state.search_clicked}/>
            </div>
        );
    }
}

export default SearchPage;
