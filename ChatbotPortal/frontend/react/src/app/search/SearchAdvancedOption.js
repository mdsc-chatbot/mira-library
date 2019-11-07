import React, {Component} from "react";
import {Accordion} from "semantic-ui-react";
import SearchByDateRange from "./SearchByDateRange";
import SearchFilter from "./SearchFilter";
import SearchByIdrange from "./SearchByIdRange";

export class SearchAdvancedOption extends Component {
    render() {
        const advanced_search_option = [
            {
                key: "date",
                title: "Date",
                content: {
                    content: (
                        <div>
                            <SearchByDateRange set_date_range_params={this.props.set_date_range_params} set_date_option_params={this.props.set_date_option_params}/>
                        </div>
                    )
                }
            },
            {
                key: "status_filter",
                title: "Status filtered",
                content: {
                    content: (
                        <div>
                            <SearchFilter set_status_search_params = {this.props.set_status_search_params}/>
                        </div>
                    )
                }
            },
            {
                key: "id_range",
                title: "Id range",
                content: {
                    content: (
                        <div>
                            <SearchByIdrange set_id_search_params={this.set_id_search_params}/>
                        </div>
                    )
                }
            }
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
            <div>
                <Accordion defaultActiveIndex={1} panels={advanced_search}/>
            </div>
        );
    }
}

export default SearchAdvancedOption;
