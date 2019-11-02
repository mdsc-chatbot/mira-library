import React, {Component} from "react";
import SearchBar from "./SearchBar";
import SearchAdvancedOption from "./SearchAdvancedOption";
import {Header} from "semantic-ui-react";
import {SecurityContext} from "../security/SecurityContext";
import axios from "axios";

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

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
                <SearchAdvancedOption />
                <SearchBar />
            </div>
        );
    }
}

export default SearchPage;
