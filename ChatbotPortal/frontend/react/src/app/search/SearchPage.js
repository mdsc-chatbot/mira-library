import React, {Component} from 'react';
import SearchBar from './SearchBar'
import SearchByDateRange from './SearchByDateRange'
import SearchByIdRange from './SearchByIdRange'
import SearchByAnything from "./SearchByAnything";

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <container>
                <SearchByAnything/>
            </container>
        );
    }
}

export default SearchPage
