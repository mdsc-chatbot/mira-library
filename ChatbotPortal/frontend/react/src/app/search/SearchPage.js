import React, {Component} from 'react';
import SearchBar from './SearchBar'
import SearchByDateRange from './SearchByDateRange'
import SearchByIdRange from './SearchByIdRange'
import SearchByAnything from "./SearchByAnything";
import SearchFilter from "./SearchFilter";

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <container>
                <SearchFilter/>
            </container>
        );
    }
}

export default SearchPage
