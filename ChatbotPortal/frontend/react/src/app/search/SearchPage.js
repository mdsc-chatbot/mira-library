import React, { Component } from "react";
import SearchBar from "./SearchBar";
import SearchByDateRange from "./SearchByDateRange";
import SearchByIdRange from "./SearchByIdRange";
import SearchByAnything from "./SearchByAnything";
import SearchFilter from "./SearchFilter";
import SearchAdvanceOption from "./SearchAdvanceOption";

import {
    Button,
    Dropdown,
    Form,
    Grid,
    Header,
    Search
} from "semantic-ui-react";

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100 }}
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
                <Search />
                <SearchAdvanceOption />
            </div>
        );
    }
}

export default SearchPage;
