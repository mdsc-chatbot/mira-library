import React, {Component} from 'react';
import SearchBar from './SearchBar'
import SearchByDateRange from './SearchByDateRange'

class SearchPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <container>
                <SearchByDateRange/>
            </container>
        );
    }
}

export default SearchPage
