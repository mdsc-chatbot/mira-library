/**
 * @file: ReviewTable.js
 * @summary: Component that renders a list of reviews and sorting options
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
import axios from "axios";
import { Table, Dropdown, Checkbox, Popup, Modal, Header, Button, Icon } from "semantic-ui-react";
import { SecurityContext } from "../contexts/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";


export default class ReviewTable extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            resources: [],
            reviews: [],
            resourceIdsWithPendingTag:[],
            pending: 'Completed Reviews',
            header: 'Review new resources and tags here!',
            resourceData: {},
            order: "newest",
            assignedOnly: true
        };
    }

    format_data = (url, resourceID, comments, rating, approval) => {
        // Get current logged in user
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        const formatted_review = {
            reviewer_user_email: reviewer,
            approved: approval,
            resource_url: url,
            resource_id: resourceID,
            review_comments: comments,
            review_rating: rating,
            final_decision: true
        };
        return formatted_review;
    };

    approve = (url, resourceID, comments, rating) => {
        const review = this.format_data(url, resourceID, comments, rating, true);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("/api/review/", review, { headers: options })
            .then(res => { })
            .catch(error => console.error(error));

        this.componentDidMount();

    };

    reject = (url, resourceID, comments, rating) => {
        const review = this.format_data(url, resourceID, comments, rating, false);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("/api/review/", review, { headers: options })
            .then(res => { })
            .catch(error => console.error(error));

        this.componentDidMount();
    };

    resourceNeedTieBreaker = (resource) => {
        if(resource.assigned_reviewer_3 != -1)
            return true

        var numOfApprovals = 0
        var numOfConflicts = 0
        var numOfRejects = 0

        if(resource.review_status_1_1 == 'approved')
            numOfApprovals +=1
        else if(resource.review_status_1_1 == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status_1_1 == 'rejected')
            numOfRejects +=1
        
        if(resource.review_status_2 == 'approved')
            numOfApprovals +=1
        else if(resource.review_status_2 == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status_2 == 'rejected')
            numOfRejects +=1

        if(resource.review_status_2_2 == 'approved')
            numOfApprovals +=1
        else if(resource.review_status_2_2 == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status_2_2 == 'rejected')
            numOfRejects +=1

        if(resource.review_status == 'approved')
            numOfApprovals +=1
        else if(resource.review_status == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status == 'rejected')
            numOfRejects +=1

        if(numOfApprovals == numOfRejects && numOfApprovals>0)
            return true
        
        return false
    }

    get_resources = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/resource/", { headers: options }).then(res => {
            this.setState({
                resources: res.data
            });
        });
    };

    get_reviews = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/api/review/", { headers: options }).then(res => {
            this.setState({
                reviews: res.data
            });
        });
    }

    get_resources_with_panding_tags = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };

        axios
            .get("/chatbotportal/resource/get-all-resources-with-pending-tags", { headers: options })
            .then(response => {
                this.setState({
                    resourceIdsWithPendingTag: response.data.map(i => (i.resourceId))
                });
            })
    }

    componentDidMount() {
        this.get_resources();
        this.get_reviews();
        this.get_resources_with_panding_tags();
    }


    completedReviews = (ids, reviews, reviews_2, currentReviewer, resourceIdsWithPendingTag) => {
        var allReviews = this.state.reviews;
        function numRevs(id) {
            var numReviews = allReviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id);
            }, 0); return numReviews
        }
        function numRevsApproved(id) {
            var numReviews = allReviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === true);
            }, 0); return numReviews
        }
        function numRevsRejected(id) {
            var numReviews = allReviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === false);
            }, 0); return numReviews
        }
        function revHasFinalDecision(id) {
            var numReviews = allReviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === true && reviews.final_decision === true);
            }, 0); return numReviews
        }
        function compareOldest(a, b) {
            if ((new Date(a.timestamp).getTime() / 1000) < (new Date(b.timestamp).getTime() / 1000)) {
                return -1;
            }
            if ((new Date(a.timestamp).getTime() / 1000) > (new Date(b.timestamp).getTime() / 1000)) {
                return 1;
            }
            return 0;
        }
        function compareNewest(a, b) {
            if ((new Date(a.timestamp).getTime() / 1000) > (new Date(b.timestamp).getTime() / 1000)) {
                return -1;
            }
            if ((new Date(a.timestamp).getTime() / 1000) < (new Date(b.timestamp).getTime() / 1000)) {
                return 1;
            }
            return 0;
        }
        function compareReviews(a, b) {
            if (numRevs(a.id) < numRevs(b.id)) {
                return -1;
            }
            if (numRevs(a.id) > numRevs(b.id)) {
                return 1;
            }
            return 0;
        }
        function compareTieBreak(resource) {
            if (revHasFinalDecision(resource.id) == 0) {
                if(resource.assigned_reviewer_3 != -1)
                    return 1

                var numOfApprovals = 0
                var numOfConflicts = 0
                var numOfRejects = 0

                if(resource.review_status_1_1 == 'approved')
                    numOfApprovals +=1
                else if(resource.review_status_1_1 == 'conflict')
                    numOfConflicts +=1
                else if(resource.review_status_1_1 == 'rejected')
                    numOfRejects +=1
                
                if(resource.review_status_2 == 'approved')
                    numOfApprovals +=1
                else if(resource.review_status_2 == 'conflict')
                    numOfConflicts +=1
                else if(resource.review_status_2 == 'rejected')
                    numOfRejects +=1

                if(resource.review_status_2_2 == 'approved')
                    numOfApprovals +=1
                else if(resource.review_status_2_2 == 'conflict')
                    numOfConflicts +=1
                else if(resource.review_status_2_2 == 'rejected')
                    numOfRejects +=1

                if(resource.review_status == 'approved')
                    numOfApprovals +=1
                else if(resource.review_status == 'conflict')
                    numOfConflicts +=1
                else if(resource.review_status == 'rejected')
                    numOfRejects +=1

                if(numOfApprovals == numOfRejects && numOfApprovals>0)
                    return -1
            
            }
            return 1;
        }
        function compareHasTag(a) {
            if(resourceIdsWithPendingTag.includes(a.id)){
                return -1;
            } 
            return 1;
        }
        
        if (this.state.order === 'oldest') {
            this.state.resources = this.state.resources.sort(compareOldest)
        } else if (this.state.order === 'newest') {
            this.state.resources = this.state.resources.sort(compareNewest)
        } else if (this.state.order === 'least reviewed') {
            this.state.resources = this.state.resources.sort(compareReviews)
        } else if (this.state.order === 'tie breakers') {
            this.state.resources = this.state.resources.sort(compareTieBreak)
        } else if (this.state.order === 'tag') {
            this.state.resources = this.state.resources.sort(compareHasTag)
        }

        

        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            (ids.includes(r.id) === true) && ((this.state.assignedOnly === true && (r.assigned_reviewer == currentReviewer || r.assigned_reviewer_2 == currentReviewer || r.assigned_reviewer_3 == currentReviewer || r.assigned_reviewer_1_1 == currentReviewer || r.assigned_reviewer_2_2 == currentReviewer)) || (this.state.assignedOnly === false)) &&
                ((reviews.has(r.id) && reviews_2.has(r.id)) && ((reviews.get(r.id)[0] === reviews_2.get(r.id)[0]) || (reviews.get(r.id)[3] && ((reviews.get(r.id)[0] !== reviews_2.get(r.id)[0]))))) ? (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>
                        {(this.context.security.is_editor|| this.context.security.is_reviewer) ?
                            (reviews.get(r.id)[1].length < 100) ?
                                reviews.get(r.id)[1] : 
                                <div>{reviews.get(r.id)[1].substring(0, 100)+' ...'}
                                <Modal
                                    trigger={<p>see more</p>,<Icon color="blue" name='arrow alternate circle right outline'/>}
                                    header='1st Reviewer Comment'
                                    content={reviews.get(r.id)[1]}
                                /></div>
                            : '---'}
                    </td>
                    <td>
                        {(this.context.security.is_editor || this.context.security.is_reviewer) ?
                            (reviews_2.get(r.id)[1].length < 100) ?
                                reviews_2.get(r.id)[1] : 
                                <div>{reviews_2.get(r.id)[1].substring(0, 100)+' ...'}
                                <Modal
                                    trigger={<p>see more</p>,<Icon color="blue" name='arrow alternate circle right outline'/>}
                                    header='2nd Reviewer Comment'
                                    content={reviews_2.get(r.id)[1]}
                                /></div>
                            : '---'}
                    </td>
                    <td>
                        {reviews.get(r.id)[0] === true ? [<div>Approved<i class="check icon green large"></i></div>] : [<div>Rejected<i class="x icon red large"></i></div>]}
                    </td>
                </tr>
            ) : (reviews_2.has(r.id))
                && ((this.state.assignedOnly === true && (r.assigned_reviewer == currentReviewer || r.assigned_reviewer_2 == currentReviewer || r.assigned_reviewer_3 == currentReviewer || r.assigned_reviewer_1_1 == currentReviewer || r.assigned_reviewer_2_2 == currentReviewer)) || (this.state.assignedOnly === false)) ? (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>
                        {(this.context.security.is_editor)
                            ? [reviews.get(r.id)[0] === true ? [<dev>Approved<Popup content={reviews.get(r.id)[1]} trigger={<i class="check icon green"></i>} /></dev>] : [<dev>Rejected<Popup content={reviews.get(r.id)[1]} trigger={<i class="x icon red "></i>}/></dev>]]
                            :
                            [reviews.get(r.id)[0] === true ? [<div>Approved<i class="check icon red"></i></div>] : [<div>Rejected<i class="x icon red"></i></div>]]
                        }
                    </td>
                    <td>
                        {(this.context.security.is_editor) ?
                            [reviews_2.get(r.id)[0] === true ? [<dev>Approved<Popup content={reviews_2.get(r.id)[1]} trigger={<i class="check icon green "></i>} /></dev>] : [<dev>Rejected<Popup content={reviews_2.get(r.id)[1]} trigger={<i class="x icon red "></i>} /></dev>]]
                            :
                            [reviews_2.get(r.id)[0] === true ? [<div>Approved<i class="check icon green "></i></div>] : [<div>Rejected<i class="x icon red "></i></div>]]

                        }
                    </td>
                    <td>
                        {(this.context.security.is_editor) ?
                            <button
                                name="approve"
                                class="positive ui button"
                                onClick={() => this.approve(r.url, r.id, reviews.get(r.id)[1], reviews.get(r.id)[2])}>Approve
                            </button>
                            : null}
                        {(this.context.security.is_editor) ?
                            <button
                                name="reject"
                                class="negative ui button"
                                onClick={() => this.reject(r.url, r.id, reviews.get(r.id)[1], reviews.get(r.id)[2])}>&nbsp;&nbsp;Reject&nbsp;&nbsp;&nbsp;
                            </button>
                            : null}
                    </td>
                </tr>
            ) : (<p></p>)
        ));
        return resources_get
    }

    switchView = () => {
        if (this.state.pending === 'Completed Reviews') {
            this.setState({ pending: 'Pending Reviews', header: 'View a list of your review actions here!' });
        } else {
            this.setState({ pending: 'Completed Reviews', header: 'Review new resources and tags here!' })
        }
    }

    handleOrder = (e, { value }) => { this.setState({ order: { value }.value }) }


    getData = (reviews, ids, currentReviewer, resourceIdsWithPendingTag) => {
        function numRevs(id) {
            var numReviews = reviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id);
            }, 0); return numReviews
        }
        function numRevsApproved(id) {
            var numReviews = reviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === true);
            }, 0); return numReviews
        }
        function numRevsRejected(id) {
            var numReviews = reviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === false);
            }, 0); return numReviews
        }
        function revHasFinalDecision(id) {
            var numReviews = reviews.reduce(function (n, reviews) {
                return n + (reviews.resource_id == id && reviews.approved === true && reviews.final_decision === true);
            }, 0); return numReviews
        }
        function compareOldest(a, b) {
            if ((new Date(a.timestamp).getTime() / 1000) < (new Date(b.timestamp).getTime() / 1000)) {
                return -1;
            }
            if ((new Date(a.timestamp).getTime() / 1000) > (new Date(b.timestamp).getTime() / 1000)) {
                return 1;
            }
            return 0;
        }
        function compareNewest(a, b) {
            if ((new Date(a.timestamp).getTime() / 1000) > (new Date(b.timestamp).getTime() / 1000)) {
                return -1;
            }
            if ((new Date(a.timestamp).getTime() / 1000) < (new Date(b.timestamp).getTime() / 1000)) {
                return 1;
            }
            return 0;
        }
        function compareReviews(a, b) {
            if (numRevs(a.id) < numRevs(b.id)) {
                return -1;
            }
            if (numRevs(a.id) > numRevs(b.id)) {
                return 1;
            }
            return 0;
        }
        function compareTieBreak(a) {
            if(resource.assigned_reviewer_3 != -1)
                return 1

            var numOfRejects = 0
            var numOfApproves = 0
            if(a.review_status_2 == 'approved')
                numOfApproves += 1
            else if(a.review_status_2 == 'rejected')
                numOfRejects +=1
            
            if(a.review_status == 'approved')
                numOfApproves += 1
            else if(a.review_status == 'rejected')
                numOfRejects +=1

            if(a.review_status_2_2 == 'approved')
                numOfApproves += 1
            else if(a.review_status_2_2 == 'rejected')
                numOfRejects +=1

            if(a.review_status_1_1 == 'approved')
                numOfApproves += 1
            else if(a.review_status_1_1 == 'rejected')
                numOfRejects +=1


            if (numOfApproves==numOfRejects && numOfApproves>0) {
                return -1;
            }
            return 1;
        }
        function compareHasTag(a) {
            if(resourceIdsWithPendingTag.includes(a.id)){
                return -1;
            } 
            return 1;
        }

        function resourceIsPending(a){
            var numOfRejects = 0
            var numOfApproves = 0
            if(a.review_status_2 == 'approved')
                numOfApproves += 1
            else if(a.review_status_2 == 'rejected')
                numOfRejects +=1
            
            if(a.review_status == 'approved')
                numOfApproves += 1
            else if(a.review_status == 'rejected')
                numOfRejects +=1

            if(a.review_status_2_2 == 'approved')
                numOfApproves += 1
            else if(a.review_status_2_2 == 'rejected')
                numOfRejects +=1

            if(a.review_status_1_1 == 'approved')
                numOfApproves += 1
            else if(a.review_status_1_1 == 'rejected')
                numOfRejects +=1


            if ((numOfApproves-numOfRejects >= 2) || 
                (numOfRejects-numOfApproves >= 2)) {
                return false;
            }
            return true;
        }

        if (this.state.order === 'oldest') {
            this.state.resources = this.state.resources.sort(compareOldest)
        } else if (this.state.order === 'newest') {
            this.state.resources = this.state.resources.sort(compareNewest)
        } else if (this.state.order === 'least reviewed') {
            this.state.resources = this.state.resources.sort(compareReviews)
        } else if (this.state.order === 'tie breakers') {
            this.state.resources = this.state.resources.sort(compareTieBreak)
        } else if (this.state.order === 'tag') {
            this.state.resources = this.state.resources.sort(compareHasTag)
        }
        
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            (!this.state.assignedOnly && (resourceIsPending(r)))
                || ((this.state.assignedOnly && (resourceIsPending(r)) && ((r.assigned_reviewer === currentReviewer && r.review_status === 'pending') || (r.assigned_reviewer_2 === currentReviewer && r.review_status_2 === 'pending') || (r.assigned_reviewer_3 === currentReviewer && r.review_status_3 === 'pending') || (r.assigned_reviewer_1_1 === currentReviewer && r.review_status_1_1 === 'pending') || (r.assigned_reviewer_2_2 === currentReviewer && r.review_status_2_2 === 'pending')))) ? (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><div><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link>{(this.context.security.is_editor) && (this.state.resourceIdsWithPendingTag.includes(r.id)) ? <i class="tags icon blue"></i> : null}</div></td>
                    <td>
                        <button class="right floated ui button"><Link to={baseRoute + "/review/" + r.id}>Review</Link></button>
                    </td>
                </tr>
            ) : (<p></p>)
        ));
        return resources_get
    }
    pendingHeader = () => {
        return <tr><th>Pending Resource</th><th></th></tr>
    }
    completedHeader = () => {
        return <tr><th>Completed Resource</th><th>#1 Review Comment</th><th>#2 Review Comment</th><th></th></tr>
    }

    sorting = (options) => {
        return <tr><th>Resource</th><th>Review Comments</th><th>Review Rating</th><th></th></tr>
    }
    render() {
        // Get current logged in user, take this function out of format_data and consolidate it later
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        const reviewsI = this.state.reviews;
        var ids = []
        reviewsI.forEach(function (item) {
            ids.push(item.resource_id)
        })

        var reviewsApproval = new Map();
        var reviewsApproval_2 = new Map();

        reviewsI.forEach(function (item) {
            if (reviewsApproval.has(item.resource_id)) {
                reviewsApproval_2.set(item.resource_id, [item.approved, item.review_comments, item.review_rating, item.final_decision])
            } else {
                reviewsApproval.set(item.resource_id, [item.approved, item.review_comments, item.review_rating, item.final_decision]);
            }

            if (item.final_decision) {
                reviewsApproval.set(item.resource_id, [item.approved, item.review_comments, item.review_rating, item.final_decision]);
            }
        })

        const choices = [
            { text: 'most recent', value: 'newest' },
            { text: 'oldest', value: 'oldest' },
            { text: 'least reviewed', value: 'least reviewed' },
            { text: 'tie breaker needed', value: 'tie breakers' },
            { text: 'new tags', value: 'tag' },
        ]

        const { value } = this.state.order;
        const resources = this.state.resources
        var viewPending = true
        return (
            <div>
                <div style={{ paddingTop: '2%', paddingLeft: '6%', paddingRight: '6%' }}>
                    <div style={{ padding: "2em 0em", textAlign: "center" }}
                        vertical>
                    </div>
                    {/* {this.state.pending === 'Completed Reviews'? */}
                    <div style={{ display: 'inline-block' }}>
                        <h4>Order Submissions By </h4>
                        <Dropdown class="ui inline dropdown"
                            name="subject"
                            placeholder='most recent'
                            selection
                            onChange={this.handleOrder}
                            options={choices}
                            value={value}
                        />
                    </div>
                    {/* :null} */}
                    <button class="ui right floated button" style={{ display: 'inline' }} onClick={() => this.switchView()}>{this.state.pending}</button>
                    {(this.context.security.is_editor) ? <Checkbox onChange={() => this.setState((prevState) => ({ assignedOnly: !prevState.assignedOnly }))} checked={this.state.assignedOnly} label="Assigned Resources Only" /> : null}
                    <div style={{ height: '500px', overflowX: "scroll", width: "100%" }}>
                        <Table class="ui celled table">
                            <thead>
                                {this.state.pending === 'Completed Reviews' ? (this.pendingHeader()) : (this.completedHeader())}
                            </thead>
                            <tbody>
                                {this.state.pending === 'Completed Reviews' ? (this.getData(this.state.reviews, ids, reviewer, this.state.resourceIdsWithPendingTag)) : (this.completedReviews(ids, reviewsApproval, reviewsApproval_2, reviewer, this.state.resourceIdsWithPendingTag))}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </div>
        );
    }
}