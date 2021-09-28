/**
 * @file: reviewResource.js
 * @summary: Component that renders a review (under resource detail componenet) and handles the review process
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
import React, { Component } from "react";
import axios, { CancelToken } from "axios";
import { Container, Form, Icon, Rating, Checkbox, Table } from "semantic-ui-react";
import { SecurityContext } from "../contexts/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ResourceResponsive from "../resource/ResourceResponsive";
import { ResourceDetailView } from "../shared";
import ReviewMatrix from "./ReviewMatrixControl";


/**
 * This class renders the Resource Detail for the logged in User
 */
export default class ResourceDetail extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {},
            rating: 1,
            comments: "No comments",
            tags: [],
            reviewData: {},
        };
    };

    get_resource_details = () => {
        const resourceID = this.props.match.params.resourceID;

        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}`, { headers: options })
            .then(res => {
                this.setState({
                    resource: res.data

                });
            });
    };

    componentDidMount() {
        this.get_resource_details();
        this.handleSearchChange();
    };

    approve = data => {
        const review = this.format_data(data, true);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("/api/review/", review, { headers: options })
            .then(res => {
            })
            .catch(error => console.error(error));


        //submit second review record in this try, if reviewer_1 == assigned_reviewer_2
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        var rs1 = this.state.resource.review_status;
        var rs2 = this.state.resource.review_status_2;
        if ((rs1 === "pending" && this.state.resource.assigned_reviewer === reviewer) &&
            (rs2 === "pending" && this.state.resource.assigned_reviewer_2 === reviewer)) {
            axios
                .post("/api/review/", review, { headers: options })
                .then(res => {
                })
                .catch(error => console.error(error));
        }


        this.update_resource_user("approved");
    };

    reject = data => {
        const review = this.format_data(data, false);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("/api/review/", review, { headers: options })
            .then(res => {
            })
            .catch(error => console.error(error));
        this.update_resource_user("rejected");
    };

    update_resource_user = (review_status) => {

        this.get_resource_details();

        console.log(submitCmd);

        if (this.state.resource.review_status === "pending" || this.state.resource.review_status_2 === "pending") {

            const reviewer = this.context.security.is_logged_in
                ? this.context.security.id
                : "Unknown user";

            //check if second approval or not
            //serializer forces us to include both review statuses in the proper state
            var rs1 = this.state.resource.review_status;
            var rs2 = this.state.resource.review_status_2;
            if (rs1 === "pending" && this.state.resource.assigned_reviewer === reviewer) rs1 = review_status;
            if (rs2 === "pending" && this.state.resource.assigned_reviewer_2 === reviewer) rs2 = review_status;
            var submitCmd = { "review_status": rs1, "review_status_2": rs2, "rating": this.state.rating, "review_comments": this.state.comments };

            const options = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.context.security.token}`
            };

            // Resource
            axios
                .put(
                    "/chatbotportal/resource/" + this.props.match.params.resourceID + "/update/",
                    submitCmd,
                    { headers: options }
                )
                .then(
                    response => {
                    },
                    error => {
                        console.log(error);
                    }
                );
            for (var i = 0, len = this.state.tags.length; i < len; i++) {
                if (this.state.tags[i].approved === true) {
                    axios
                        .put(
                            "/chatbotportal/resource/" + this.state.tags[i].id + "/updatetags/",
                            { "approved": true },
                            { headers: options }
                        )
                        .then(
                            response => {
                            },
                            error => {
                                console.log(error);
                            }
                        );
                }
            }
            // User
            if (review_status === "approved") {
                axios
                    .put(`/chatbotportal/authentication/${this.state.resource.created_by_user_pk}/update/approved_submissions/`, '', {
                        headers: { 'Authorization': `Bearer ${this.context.security.token}` }
                    })
                    .then(
                        response => { },
                        error => {
                            console.log(error);
                        }
                    );
            }
        }
    };

    format_data = (data, approval) => {
        const resourceID = this.props.match.params.resourceID;
        // Get current logged in user
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        const formatted_review = {
            reviewer_user_email: reviewer,
            approved: approval,
            resource_url: data.url,
            resource_id: resourceID,
            review_comments: this.state.comments,
            review_rating: this.state.rating,
            question_answers: JSON.stringify(this.state.reviewData),
        };
        return formatted_review;
    };

    handleRate = (event, data) => {
        this.setState({ rating: data.rating });
    };

    handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
    };

    downloadAttachment = () => {
        // Having the permission header loaded
        //TODO: Fix this. This file should be using the shared component for viewing a resource.
        // const options = {
        //     'Content-Type': 'application/json',
        //     'Authorization': `Bearer ${this.context.security.token}`
        // };
        // axios
        //     .get(`/chatbotportal/resource/download-attachment/${this.state.resource.id}`, {headers: options})
        //     .then(response => {
        //         const fileName = response.headers["content-disposition"].split(
        //             '"'
        //         )[1];
        //         fileDownload(response.data, fileName);
        //     });
    };

    handleSearchChange = () => {
        const resourceID = this.props.match.params.resourceID;
        // Fetch search results
        axios
            .get(`/chatbotportal/resource/get-tags/${resourceID}`, '',
                {
                    headers: { Authorization: `Bearer ${this.context.security.token}` }
                }
            )

            .then(response => {
                this.setState({
                    tags: response.data
                });
            })
    };

    updateTagApproval = (id) => {
        this.setState(state => {
            const tags = this.state.tags.map((item) => {
                if (item.id === id) {
                    if (item.approved === true) {
                        return item.approved = false;
                    } else {
                        return item.approved = true;
                    }

                } else {
                    return item;
                }
            });
        });
    };

    render() {
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";
        return (

            <SecurityContext.Consumer>
                {(securityContext) => (
                    <div>
                        {securityContext.security.is_logged_in ?

                            <ResourceResponsive
                                resource_component={
                                    <div>
                                        <ResourceDetailView resource={this.state.resource} tagsGot={this.state.tags} viewer={reviewer} />
                                        <div>
                                            {/* {this.state.resource.tags && this.state.resource.tags.length > 0? ( 
                                        <Table class="ui celled table">
                                            <thead>
                                                <tr><th>tag ID</th><th>Tag Name</th><th>Approve</th></tr>
                                            </thead>
                                            <tbody>
                                                {this.state.tags.map(tag => (
                                                    tag.approved !== true ?(
                                                        <tr key={tag} ref={tr => this.results = tr}>
                                                        <td>{tag.id}</td>
                                                        <td>{tag.name}</td>
                                                        <td><Checkbox onChange={() => this.updateTagApproval(tag.id)} toggle/></td>
                                                        </tr>
                                                    ):('')
                                                ))}
                                            </tbody>
                                        </Table>
                                    ) : null} */}
                                        </div>
                                        <ReviewMatrix
                                            onChange={reviewData => this.setState({ reviewData })}
                                        />
                                        <div>
                                            <div class="ui form">
                                                <div
                                                    class="required field"
                                                    style={{ display: "block" }}
                                                >
                                                    <h4>Based on the answers to all of the above questions, rate the overall quality of the resource.</h4>
                                                    <Form.Field>
                                                        <Rating
                                                            name="rating"
                                                            onRate={this.handleRate}
                                                            onChange={this.handleChange}
                                                            value={this.state.rating}
                                                            defaultRating={this.state.rating}
                                                            maxRating={5}
                                                            icon="star"
                                                            size="massive"
                                                        />
                                                    </Form.Field>
                                                </div>
                                                <div
                                                    class="required field"
                                                    style={{ display: "block" }}
                                                >
                                                    <h4>Review Comments</h4>
                                                    <Form.TextArea
                                                        name="comments"
                                                        onChange={this.handleChange}
                                                        value={this.state.comments}
                                                        placeholder="Enter any comments about this resource"
                                                    />
                                                </div>
                                                <div style={{ display: "block" }}>
                                                    <Link to={baseRoute + "/review/"}>
                                                        <button
                                                            name="approve"
                                                            class="positive ui button"
                                                            onClick={() => this.approve(this.state.resource)}
                                                        >
                                                            Approve
                                                        </button>
                                                    </Link>
                                                    <Link to={baseRoute + "/review/"}>
                                                        <button
                                                            name="reject"
                                                            class="negative ui button"
                                                            onClick={() => this.reject(this.state.resource)}
                                                        >
                                                            &nbsp;&nbsp;Reject&nbsp;&nbsp;
                                                        </button>
                                                    </Link>
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                }
                            ></ResourceResponsive>


                            : null}
                    </div>)}
            </SecurityContext.Consumer>
        );
    }
}
