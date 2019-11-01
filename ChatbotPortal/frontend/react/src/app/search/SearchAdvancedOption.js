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
                            <SearchByDateRange/>
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
                            <SearchFilter/>
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
                            <SearchByIdrange/>
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
