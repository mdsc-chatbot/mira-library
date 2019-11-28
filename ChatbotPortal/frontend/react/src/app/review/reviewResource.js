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
import React, {Component} from "react";
import axios, {CancelToken} from "axios";
import {Container, Form, Icon, Rating, Checkbox, Table} from "semantic-ui-react";
import {SecurityContext} from "../contexts/SecurityContext";
import {baseRoute} from "../App";
import {Link} from "react-router-dom";
import ResourceResponsive from "../resource/ResourceResponsive";
import { ResourceDetailView } from "../shared";


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
        };
    }

    get_resource_details = () => {
        const resourceID = this.props.match.params.resourceID;

        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}`, {headers: options})
            .then(res => {
                this.setState({
                    resource: res.data
                    
                });
            });
    };

    componentDidMount() {
        this.get_resource_details();
        this.handleSearchChange();
    }

    approve = data => {
        const review = this.format_data(data, true);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("/api/review/", review, {headers: options})
            .then(res => {
            })
            .catch(error => console.error(error));
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
            .post("/api/review/", review, {headers: options})
            .then(res => {
            })
            .catch(error => console.error(error));
        this.update_resource_user("rejected");
    };

    update_resource_user = (review_status) => {

        this.get_resource_details();
        if (this.state.resource.review_status === "pending") {

            const options = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.context.security.token}`
            };

            // Resource
            axios
                .put(
                    "/chatbotportal/resource/" + this.props.match.params.resourceID + "/update/",
                    {"review_status": review_status, "rating": this.state.rating},
                    {headers: options}
                )
                .then(
                    response => {
                    },
                    error => {
                        console.log(error);
                    }
                );
            for (var i = 0, len = this.state.tags.length; i < len; i++) {
                    if (this.state.tags[i].approved === true){
                        axios
                            .put(
                                "/chatbotportal/resource/" + this.state.tags[i].id + "/updatetags/",
                                {"approved": true},
                                {headers: options}
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
                        response => {},
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
            review_rating: this.state.rating
        };
        return formatted_review;
    };

    handleRate = (event, data) => {
        this.setState({rating: data.rating});
    };

    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
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
                    headers: {Authorization: `Bearer ${this.context.security.token}`}
                }
            )
            
            .then(response=>{
                this.setState({
                    tags: response.data
                });
            })
        };
    
    updateTagApproval = (id, status) =>{
        this.setState(state => {
            const tags = this.state.tags.map((item) => {
                if (item.id === id) {
                  return item.approved=status;
                  
                } else {
                  return item;
                }
            });
        });
    }

    render() {
        return (
            <div
                style={{paddingTop: 30, paddingLeft: 100, paddingRight: 100, paddingBottom: 30,}}
            >
                <SecurityContext.Consumer>
                    {(securityContext) => (
                        <div>
                            {securityContext.security.is_logged_in ?
                                <div>

                                    <Container>
                                    <ResourceResponsive
                                        resource_component={<ResourceDetailView resource={this.state.resource} tagsGot={this.state.tags} />}
                                    ></ResourceResponsive>
                                    </Container>
                                    
                                    <Container>
                                    {this.state.resource.tags && this.state.resource.tags.length > 0? ( 
                                        <Table class="ui celled table">
                                            <thead>
                                                <tr><th>tag ID</th><th>Tag Name</th><th></th></tr>
                                            </thead>
                                            <tbody>
                                                {this.state.tags.map(tag => (
                                                    tag.approved !== true ?(
                                                        <tr key={tag} ref={tr => this.results = tr}>
                                                        <td>{tag.id}</td>
                                                        <td>{tag.name}</td>
                                                        <td>
                                                        <button class="positive ui button" onClick={() => this.updateTagApproval(tag.id, true)}>Approve</button>
                                                        <button class="negative ui button" onClick={() => this.updateTagApproval(tag.id, false)}>Reject</button>
                                                        </td>
                                                        <td><Checkbox disabled/></td>
                                                        </tr>
                                                    ):('')
                                                ))}
                                            </tbody>
                                        </Table>
                                    ) : null}
                                    </Container>

                                    <Container style={{width: "50%", height: "10%"}}>
                                        <h2>Submit Review</h2>
                                        <div class="ui form">
                                            <div
                                                class="required field"
                                                style={{display: "block"}}
                                            >
                                                <h4>Submission Quality</h4>
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
                                                style={{display: "block"}}
                                            >
                                                <h4>Review Comments</h4>
                                                <Form.TextArea
                                                    name="comments"
                                                    onChange={this.handleChange}
                                                    value={this.state.comments}
                                                    placeholder="Enter any comments about this resource"
                                                />
                                            </div>
                                            <div style={{display: "block"}}>
                                                <Link to={baseRoute + "/review/"}>
                                                    <button
                                                        class="positive ui button"
                                                        onClick={() =>
                                                            this.approve(this.state.resource)
                                                        }
                                                    >
                                                        Approve
                                                    </button>
                                                </Link>
                                                <Link to={baseRoute + "/review/"}>
                                                    <button
                                                        class="negative ui button"
                                                        onClick={() =>
                                                            this.reject(this.state.resource)
                                                        }
                                                    >
                                                        Reject
                                                    </button>
                                                </Link>
                                            </div>
                                        </div>
                                    </Container>
                                </div> : null}
                        </div>)}
                </SecurityContext.Consumer>
            </div>
        );
    }
}
