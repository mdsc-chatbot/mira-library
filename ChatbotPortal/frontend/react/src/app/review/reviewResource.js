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
import { Container, Form, Icon, Rating, Checkbox, Table, Card, Image, Button, Segment, Dropdown } from "semantic-ui-react";
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
        this.time = 0;
        this.myTimer;

        this.state = {
            resource: {},
            rating: 1,
            comments: "No comments",
            tags: [],
            TagCatOptions: [],
            reviewData: {},
        };

        window.addEventListener('popstate', function (e) {
            var state = e.state;
            if (state !== null) {
                clearInterval(this.myTimer)
            }
        });
            
    };

    get_resource_details = () => {
        const resourceID = this.props.match.params.resourceID;

        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}/`, { headers: options })
            .then(res => {
                this.setState({
                    resource: res.data
                });
            });
    };

    componentDidMount() {
        this.get_resource_details();
        this.handleSearchChange();  
        this.fetchTags();
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
        var rs3 = this.state.resource.review_status_3;
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


        if (this.state.resource.review_status === "pending" || this.state.resource.review_status_2 === "pending" ||
            this.state.resource.review_status === "conflict" || this.state.resource.review_status_2 === "conflict" ||
            this.state.resource.review_status_3 === "pending" || this.state.resource.review_status_3 === "conflict" ||
            this.state.resource.review_status_2_2 === "pending" || this.state.resource.review_status_2_2 === "conflict" ||
            this.state.resource.review_status_1_1 === "pending" || this.state.resource.review_status_1_1 === "conflict") {

            const reviewer = this.context.security.is_logged_in
                ? this.context.security.id
                : "Unknown user";

            //check if second approval or not
            //serializer forces us to include both review statuses in the proper state
            var rs1 = this.state.resource.review_status;
            var rs2 = this.state.resource.review_status_2;
            var rs3 = this.state.resource.review_status_3;
            var rs4 = this.state.resource.review_status_1_1;
            var rs5 = this.state.resource.review_status_2_2;

            var submitCmd = {
                // "review_status": rs1,
                // "review_status_2": rs2,
                // "review_status_3": rs3,
                "rating": this.state.rating,
                "review_comments": this.state.comments
            };

            if ((rs1 === "pending" || rs1 === "conflict") && this.state.resource.assigned_reviewer === reviewer) submitCmd['review_status'] = review_status
            if ((rs2 === "pending" || rs2 === "conflict") && this.state.resource.assigned_reviewer_2 === reviewer) submitCmd['review_status_2'] = review_status
            if ((rs3 === "pending" || rs3 === "conflict") && this.state.resource.assigned_reviewer_3 === reviewer) submitCmd['review_status_3'] = review_status
            if ((rs4 === "pending" || rs4 === "conflict") && this.state.resource.assigned_reviewer_1_1 === reviewer) submitCmd['review_status_1_1'] = review_status
            if ((rs5 === "pending" || rs5 === "conflict") && this.state.resource.assigned_reviewer_2_2 === reviewer) submitCmd['review_status_2_2'] = review_status
            

            const options = {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.context.security.token}`
            };

            //stop timer
            clearInterval(this.myTimer)

            // Resource
            axios
                .put(
                    "/chatbotportal/resource/" + this.props.match.params.resourceID + "/updatepartial/",
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
            review_time_sec: this.time
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

    updateTagCategory = (id, value) => {
        this.setState(state => {
            const tags = this.state.tags.map((item) => {
                if (item.id === id) {
                    console.log('updateeeeed.')
                    return item.tag_category = value;
                } else {
                    return item;
                }
            });
        });
    };


    updateTags = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        for (var i = 0, len = this.state.tags.length; i < len; i++) {
            if (this.state.tags[i].approved === true) {
                axios
                    .put(
                        "/chatbotportal/resource/" + this.state.tags[i].id + "/updatetags/",
                        { "approved": true , "tag_category": this.state.tags[i].tag_category},
                        { headers: options }
                    )
                    .then(
                        response => {
                            console.log('re',response);
                        },
                        error => {
                            console.log('er',error);
                        }
                    );
            }
        }
    }

    handleAssign = (value, field, tagId) => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
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
    }

    myTimer = () => {
        this.time += 1;
        //console.log('timer',this.time)
    }

    fetchTags = () => {
        const headers = {};
        if (this.context.security.token) {
            headers['Authorization'] = `Bearer ${this.context.security.token}`;
        }

        axios
            .get("/api/public/tags", {
                headers
            })
            .then(res => {
                this.getTagCatOptions(res.data);
            });
    };


    getTagCatOptions = (allPossibleTags) => {
        var tagOptions = [];
        var tagSets = [];
        for (var i = 0; i < allPossibleTags.length; i++) {
            const newOption = {
                key: allPossibleTags[i].tag_category,
                value: allPossibleTags[i].tag_category,
                text: allPossibleTags[i].tag_category
            }
            if(!tagSets.includes(newOption.key)){
                tagSets.push(newOption.key)
                tagOptions.push(newOption)
            }
        }

        this.setState({TagCatOptions:tagOptions})
    }

    render() {
        //start timer
        this.myTimer = setInterval(this.myTimer, 1000);

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
                                            <br />
                                            {
                                                ((this.context.security.is_editor) && (this.state.tags) && (this.state.tags.filter(tag=>tag.approved === false).length > 0) ) ? (
                                                    <Segment basic>
                                                        <Card fluid>
                                                            <Card.Content>
                                                                <Card.Header><h2>Tags</h2></Card.Header>
                                                            </Card.Content>
                                                            <Card.Content extra>
                                                                <Table class="ui definition table">
                                                                    <thead>
                                                                        <tr><th>tag ID</th><th>Tag Name</th><th>Tag Category</th><th>Approve</th></tr>
                                                                    </thead>
                                                                    <tbody>
                                                                        {this.state.tags.map(tag => (
                                                                            tag.approved === false ? (
                                                                                <tr key={tag.id} ref={tr => this.results = tr}>
                                                                                    <td>{tag.id}</td>
                                                                                    <td>{tag.name}</td>
                                                                                    <td>
                                                                                        {<Dropdown ui read search selection options={this.state.TagCatOptions} defaultValue={tag.tag_category} onChange={(event, { value }) => this.updateTagCategory(tag.id, value)} />}
                                                                                    </td>
                                                                                    <td><Checkbox onChange={() => this.updateTagApproval(tag.id)} toggle /></td>
                                                                                </tr>
                                                                            ) : (null)
                                                                        ))}
                                                                    </tbody>
                                                                </Table>,
                                                                <button
                                                                    name="update_tags"
                                                                    class="positive ui button"
                                                                    onClick={() => {
                                                                        this.updateTags()
                                                                        event.target.parentElement.parentElement.parentElement.remove()
                                                                    }
                                                                    }>
                                                                    Update Tags
                                                                </button>
                                                            </Card.Content>
                                                        </Card>
                                                    </Segment>
                                                ) : null


                                            }
                                            {((this.state.resource.assigned_reviewer_2 == reviewer) || (this.state.resource.assigned_reviewer == reviewer) || (this.state.resource.assigned_reviewer_3 == reviewer) || (this.state.resource.assigned_reviewer_2_2 == reviewer) || (this.state.resource.assigned_reviewer_1_1 == reviewer)) ?
                                                ([<Segment basic textAlign='center'>
                                                    <Card fluid>
                                                        <Card.Content>
                                                            <Card.Header><h1>Conflict of Interests OR any other reason to skip this resource!</h1></Card.Header>
                                                            <Card.Description>
                                                                <strong>Before you begin this review, please consider whether or not you might have a conflict of interest in reviewing this resource. Could you potentially have a conflict of interest in reviewing this resource? If so, no problem! Please indicate here and we will reassign the resource to another reviewer.</strong>
                                                                <p>A conflict of interest occurs when an individual’s personal interests – family, friendships, financial, or social factors – could compromise his or her judgment, decisions, or actions (adapted from <a target="_blank" href="https://compliance.ucf.edu/understanding-conflict-of-interest/">here</a>).</p>
                                                            </Card.Description>
                                                        </Card.Content>
                                                        <Card.Content extra>
                                                            <div className='ui two buttons'>
                                                                <Button
                                                                    basic
                                                                    color='green'
                                                                    onClick={(event) => {
                                                                        event.target.parentElement.parentElement.parentElement.parentElement.remove()
                                                                    }
                                                                    }>
                                                                    Continue
                                                                </Button>
                                                                <Button
                                                                    basic
                                                                    color='red'
                                                                    onClick={() => {
                                                                        this.update_resource_user("conflict")
                                                                        setTimeout(() => {
                                                                            var url = window.location.origin + '/chatbotportal/app/review';
                                                                            window.location.href = url;
                                                                        }, 300);
                                                                    }}>
                                                                    I do not review this resource (stop review)
                                                                </Button>
                                                            </div>
                                                        </Card.Content>
                                                    </Card>
                                                </Segment>
                                                    ,
                                                <ReviewMatrix
                                                    onChange={reviewData => this.setState({ reviewData })}
                                                />
                                                    ,
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
                                                                    onClick={() => this.reject(this.state.resource)}>
                                                                    &nbsp;&nbsp;Reject&nbsp;&nbsp;&nbsp;
                                                                </button>
                                                            </Link>
                                                        </div>
                                                    </div>
                                                </div>])
                                                : <Segment basic textAlign='center'>
                                                    <Card fluid>
                                                        <Card.Content>
                                                            <Card.Header><h1>Not Assigned Resource!</h1></Card.Header>
                                                            <Card.Description>
                                                                <strong>You are not assigned to this resource as a reviewer.</strong>
                                                            </Card.Description>
                                                        </Card.Content>
                                                    </Card>
                                                </Segment>

                                            }
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

