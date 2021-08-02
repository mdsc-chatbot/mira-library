/**
 * @file: SearchPage.js
 * @summary: Renders the Search related UI and declares search related functions that calls the backend APIs
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
import {
    Button,
    Checkbox,
    Container,
    Form,
    FormGroup,
    Header,
    Responsive,
    Segment,
    Sidebar,
    SidebarPushable,
    SidebarPusher
} from "semantic-ui-react";
import {SecurityContext} from "../contexts/SecurityContext";
import styles from "./ManageReviews.css"

class ManageReviews extends Component {

    /**
     * This constructor initializes the state that is required for the search app.
     * @param props = Properties passed down from the parent component
     */
    constructor(props) {
        super(props);

        /**
         * This is the state of this component.
         * @type {{end_date: string, start_submission: string, is_active: string, is_superuser: string, is_reviewer: string, is_staff: string, start_id: string, end_id: string, loadedData: [], search_string: string, url: string, search_option: string, end_submission: string, search_clicked: boolean, start_date: string}}
         */
        this.state = {
            search_clicked: false,
            loadedData: [],

            is_active: "''",
            is_reviewer: "''",
            is_staff: "''",
            is_superuser: "''",

            search_option: "''",
            start_date: "''",
            end_date: "''",

            start_id: "''",
            end_id: "''",

            start_submission: "''",
            end_submission: "''",
            submission_range_option: "''",

            search_string: '',

            url: "/chatbotportal/authentication/super/search/status/''/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search=",

            sidebar_visible: true,
            checkbox_visible: false,
            width: "thin",
            animation: "slide out"
        };
    }


    /**
     * This renders the search related components
     * @returns {*}
     */
    render() {
        return (
            <SecurityContext.Consumer>
                {(securityContext) => (
                    <Responsive as={SidebarPushable} minWidth={320} onUpdate={this.set_sidebar_visibility}>
                        {securityContext.security.is_logged_in ?
                            <div>Under Construction.</div>
                            : null}
                    </Responsive>
                )}
            </SecurityContext.Consumer>
        );
    }
}

export default ManageReviews;
