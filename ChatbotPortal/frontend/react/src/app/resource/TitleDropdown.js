/**
 * @file: TagsDropDown.js
 * @summary: Component that allows user to search and input tags in ResourceSubmitForm.js
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @copyright: Copyright (c) 2019 BOLDDUC LABORATORY
 * @credits: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 * @version: 1.0
 * @maintainer: BOLDDUC LABORATORY
 */

/**
 * MIT License
 *
 * Copyright (c) 2019 BOLDDUC LABORATORY
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import React from 'react';
import PropTypes from 'prop-types';
import axios, {CancelToken} from 'axios';
import {Dropdown, Responsive, Segment, SegmentGroup} from 'semantic-ui-react';
import {SecurityContext} from "../contexts/SecurityContext";


export default class TitleDropdown extends React.Component {
    static contextType = SecurityContext;

    static mapResponseToDropdownOption = resource => ({
        text: resource.title
    });

    constructor(props) {
        super(props);
        this.state = {
            searchQuery: '',
            titleOptions: [], // options to show to user (to click)
            searchRequestCancelToken: null,
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.value !== this.props.value) {
            this.setState({searchQuery:this.props.value});
        }
    }

    handleChange = (event, data) => {
        // Change value
        let searchQuery = event.target.textContent.substring(3);
        this.setState({searchQuery});
    };

    handleSearch = (options, query) => {
        let noptions = options.filter((opt) => opt.text.toLowerCase().includes(query.toLowerCase()));
        if(noptions[0] && noptions[0].text !== "Similar Resources:"){
            noptions.unshift({text: "Similar Resources:"});
        }
        return noptions;
      };

    handleSearchChange = (event, {searchQuery}) => {
        // Cancel previous search requests if possible
        if (this.state.searchRequestCancelToken) {
            this.state.searchRequestCancelToken.cancel()
        }

        // Prepare for promise cancellation
        const source = CancelToken.source();

        axios
        .get(
            `/api/public/resources`,
            {
                params: {
                    page: 1,
                    search: searchQuery,
                    tags: [],
                    categories: [],
                    sort: 0
                }
            },
            {
                headers: { Authorization: `Bearer ${this.context.security.token}` }
            }
        )
        .then(res => {
            let titleOptions = [];
            if (res.data) {
                titleOptions = res.data.results.filter(resource => resource.review_status === "approved").map(TitleDropdown.mapResponseToDropdownOption);
                for (var i=0; i < titleOptions.length; i++) {
                    titleOptions[i].text = '-> ' + titleOptions[i].text;
                }
                if(titleOptions[0] && titleOptions[0].text !== "Similar Resources:"){
                    titleOptions.unshift({text: "Similar Resources:"})
                }
            }
            this.setState({titleOptions})
        });

        this.setState({
            searchQuery: searchQuery,
            searchRequestCancelToken: source
        })
        this.props.onChange(searchQuery);
    };

    render() {
        return (
            <React.Fragment>
                <Dropdown
                    fluid
                    selection
                    onChange={this.handleChange}
                    onSearchChange={this.handleSearchChange}
                    options={this.state.titleOptions}
                    placeholder='Enter Resource Title'
                    search={this.handleSearch}
                    searchQuery={this.state.searchQuery}
                />
            </React.Fragment>
        );
    }
}
