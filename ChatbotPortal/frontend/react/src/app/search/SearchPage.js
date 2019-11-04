import React, {Component} from "react";
import SearchTable from "./SearchTable";
import SearchAdvancedOption from "./SearchAdvancedOption";
import {Header} from "semantic-ui-react";
import {SecurityContext} from "../security/SecurityContext";
import axios from "axios";

class SearchPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            is_advance_used: false
        };
    }

    handle_result_change = (results) => {
        this.setState({
            results,
            is_advance_used : true
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
                <SearchAdvancedOption handle_result_change = {this.handle_result_change}/>
                <SearchTable loadedData = {this.state.results} is_advance_used = {this.state.is_advance_used}/>
            </div>
        );
    }
}

export default SearchPage;
