import React, {Component} from "react";
import {Accordion} from "semantic-ui-react";
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
                key: "status_filter",
                title: "Status filtered",
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
                title: "Id range",
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
                title: "Submission range",
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
                <Accordion defaultActiveIndex={1} panels={advanced_search}/>
            </div>
        );
    }
}

export default SearchAdvancedOption;
