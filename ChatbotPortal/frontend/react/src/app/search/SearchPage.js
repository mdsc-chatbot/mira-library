import React, { Component } from "react";
import SearchBar from "./SearchBar";
import SearchByDateRange from "./SearchByDateRange";
import SearchByIdRange from "./SearchByIdRange";
import SearchByAnything from "./SearchByAnything";
import SearchFilter from "./SearchFilter";
import SearchAdvancedOption from "./SearchAdvancedOption";

import {
    Button,
    Dropdown,
    Form,
    Grid,
    Header,
    Search
} from "semantic-ui-react";
import axios from "axios";
import {SecurityContext} from "../security/SecurityContext";

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    static contextType = SecurityContext;

    render() {
        return (

            <div
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100, height: 600 }}
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
                {/*<Search />*/}
                <SearchAdvancedOption />
                <SearchBar />
            </div>
        );
    }
}

export default SearchPage;
