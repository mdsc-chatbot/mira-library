/**
 * @file: SearchAdvancedOption.js
 * @summary: This component creates the accordion required for showing advanced search filters.
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

import React, {Component} from "react";
import {Accordion, Header, Label} from "semantic-ui-react";
import SearchByDateRange from "./SearchByDateRange";
import SearchFilter from "./SearchFilter";
import SearchByIdRange from "./SearchByIdRange";
import SearchBySubmissionRange from "./SearchBySubmissionRange";

export class SearchAdvancedOption extends Component {
    render() {
        const advanced_search_option = [
            {
                key: "date",
                title: "Date",
                content: {
                    content: (
                        <div id='search_by_date'>
                            <SearchByDateRange set_date_range_params={this.props.set_date_range_params}
                                               set_date_option_params={this.props.set_date_option_params}/>
                        </div>
                    )
                }
            },
            {
                key: "needapproval_filter",
                title: "Status",
                content: {
                    content: (
                        <div id='search_by_filter'>
                            <SearchFilter set_status_search_params={this.props.set_status_search_params}/>
                        </div>
                    )
                }
            },
            {
                key: "status_filter",
                title: "Status",
                content: {
                    content: (
                        <div id='search_by_filter'>
                            <SearchFilter set_status_search_params={this.props.set_status_search_params}/>
                        </div>
                    )
                }
            },
            {
                key: "id_range",
                title: "By Id",
                content: {
                    content: (
                        <div id='search_by_id'>
                            <SearchByIdRange set_id_search_params={this.props.set_id_search_params}/>
                        </div>
                    )
                }
            },
            {
                key: "submission_range",
                title: "By submission",
                content: {
                    content: (
                        <div id='search_by_submission'>
                            <SearchBySubmissionRange
                                set_submission_search_params={this.props.set_submission_search_params}/>
                        </div>
                    )
                }
            },
        ];

        const advanced_search = [
            {
                key: "advanced_search",
                title: "Advanced search",
                content: {
                    content: (
                        <div style={{paddingLeft: 20, marginTop: -20}}>
                            <Accordion.Accordion
                                panels={advanced_search_option}
                                exclusive={false}
                            />
                        </div>
                    )
                }
            }
        ];

        return (
            <div id='advanced_search_accordian'>
                <Header content='Search Filter' color="blue" size="medium"/>
                <Accordion
                    panels={advanced_search_option}
                    exclusive={false}
                />
            </div>
        );
    }
}

export default SearchAdvancedOption;
