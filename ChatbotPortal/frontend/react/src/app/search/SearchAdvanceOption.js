import React, { Component } from "react";
import { Accordion, Icon } from "semantic-ui-react";
import SearchByDateRange from "./SearchByDateRange";
import SearchFilter from "./SearchFilter";
import SearchByIdrange from "./SearchByIdRange";

export class SearchAdvanceOption extends Component {
    render() {
        const advance_search_option = [
            {
                key: "date",
                title: "Date",
                content: {
                    content: (
                        <div>
                            <SearchByDateRange />
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
                            <SearchFilter />
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
                            <SearchByIdrange />
                        </div>
                    )
                }
            }
        ];

        const advance_search = [
            {
                key: "advance_search",
                title: "Advance search",
                content: {
                    content: (
                        <div style={{ paddingLeft: 20, marginTop: -20 }}>
                            <Accordion.Accordion
                                panels={advance_search_option}
                                exclusive={false}
                            />
                        </div>
                    )
                }
            }
        ];

        return (
            <div>
                <Accordion defaultActiveIndex={1} panels={advance_search} />
            </div>
        );
    }
}

export default SearchAdvanceOption;
