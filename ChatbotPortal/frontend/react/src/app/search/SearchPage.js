import React, {Component} from 'react';
import SearchBar from './SearchBar'
import SearchByDateRange from './SearchByDateRange'
import SearchByIdRange from './SearchByIdRange'

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <container>
                <SearchByIdRange/>
            </container>
        );
    }
}

export default SearchPage
