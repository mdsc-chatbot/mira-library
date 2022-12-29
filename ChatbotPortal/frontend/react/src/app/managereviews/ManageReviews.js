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
import { Table, Popup, Dropdown, Grid } from "semantic-ui-react";
import { SecurityContext } from "../contexts/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ReviewPopover from "../review/ReviewPopover"


export default class ManageReviews extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            resources: [],
            reviews: [],
            users: [],
            pending: 'Completed Reviews',
            header: 'Review new resources and tags here!',
            resourceData: {},
            order: "newest"
        };
    }

    get_resources = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/resource", { headers: options }).then(res => {
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
        axios.get("/api/review", { headers: options }).then(res => {
            this.setState({
                reviews: res.data
            });
        });
    }


    get_users = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/authentication/super/search/status/1/1/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search=&page_size=100", { headers: options }).then(res => {
            this.setState({
                users: res.data.results
            });
            console.log('users: ' + res.data.results.length);
        });
    }

    componentDidMount() {
        this.get_resources();
        this.get_reviews();
        this.get_users();
    }


    handleOrder = (e, { value }) => { this.setState({ order: { value }.value }) }

    handleAssign = (field, value, rid) => {
        var submitCmd = {}
        submitCmd[field] = value;

        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios
            .put(
                "/chatbotportal/resource/" + rid + "/updatepartial/",
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
    }

    getData = (reviews, ids, currentReviewer) => {
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
            if ((a.review_status_2 === 'approved' && a.review_status === 'rejected')
                || (a.review_status === 'approved' && a.review_status_2 === 'rejected')) {
                return -1;
            }
            return 1;
        }
        function compareInterestConflict(a) {
            if (a.review_status_2 === 'conflict' || a.review_status === 'conflict') {
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
        } else if (this.state.order === 'conflict') {
            this.state.resources = this.state.resources.sort(compareInterestConflict)
        }

        //map users for assignment dropdown
        var userOptions = [];
        for (var i = 0; i < this.state.users.length; i++) {
            userOptions.push(
                {
                    key: this.state.users[i].id,
                    value: this.state.users[i].id,
                    text: this.state.users[i].first_name + " " + this.state.users[i].last_name
                }
            )
        }
        //add unassigned field
        userOptions.push(
            {
                key: -1,
                value: -1,
                text: "Unassigned"
            }
        )
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            // r.review_status !== "approved" || r.review_status_2 !== "approved" 
            (!this.resourceIsApproved(r)) ? (
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>
                        <h4>{r.review_status === "approved" ? (<p><i class="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer}/> </p>) : r.review_status === "pending" ? (<p><i class="x icon"></i> pending</p>) : r.review_status === "conflict" ? (<p><i class="red stop circle outline icon"></i>Conflict of Interest</p>) : (<p><i class="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer}/></p>) }
                            {<Dropdown ui read search selection options={userOptions} defaultValue={r.assigned_reviewer} onChange={(event, { value }) => this.handleAssign("assigned_reviewer", value, r.id)} />}</h4>
                    </td>
                    <td>
                        <h4>{r.review_status_2 === "approved" ? (<p><i class="green check icon "></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2}/></p>) : r.review_status_2 === "pending" ? (<p><i class="x icon "></i> pending</p>) : r.review_status_2 === "conflict" ? (<p><i class="red stop circle outline icon"></i> Conflict of Interest</p>) : (<p><i class="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2}/></p>)}
                            {<Dropdown ui red search selection options={userOptions} defaultValue={r.assigned_reviewer_2} onChange={(event, { value }) => this.handleAssign("assigned_reviewer_2", value, r.id)} />}</h4>
                    </td>
                    <td>
                        <h4>{r.review_status_1_1 === "approved" ? (<p><i class="green check icon "></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_1_1}/></p>) : r.review_status_1_1 === "pending" ? (<p><i class="x icon "></i> pending</p>) : r.review_status_1_1 === "conflict" ? (<p><i class="red stop circle outline icon"></i> Conflict of Interest</p>) : (<p><i class="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_1_1}/></p>)}
                            {<Dropdown ui red search selection options={userOptions} defaultValue={r.assigned_reviewer_1_1} onChange={(event, { value }) => this.handleAssign("assigned_reviewer_1_1", value, r.id)} />}</h4>
                    </td>
                    <td>
                        <h4>{r.review_status_2_2 === "approved" ? (<p><i class="green check icon "></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2_2}/></p>) : r.review_status_2_2 === "pending" ? (<p><i class="x icon "></i> pending</p>) : r.review_status_2_2 === "conflict" ? (<p><i class="red stop circle outline icon"></i> Conflict of Interest</p>) : (<p><i class="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2_2}/></p>)}
                            {<Dropdown ui red search selection options={userOptions} defaultValue={r.assigned_reviewer_2_2} onChange={(event, { value }) => this.handleAssign("assigned_reviewer_2_2", value, r.id)} />}</h4>
                    </td>
                    {(this.resourceNeedTieBreaker(r)) ?
                    (<td>
                        <h4>{(r.review_status_3 === "approved") ? (<p><i class="green check icon "></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_3}/></p>) : r.review_status_3 === "pending" ? (<p><i class="x icon "></i> pending</p>) : r.review_status_3 === "conflict" ? (<p><i class="red stop circle outline icon"></i> Conflict of Interest</p>) : (<p><i class="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_3}/></p>)}
                            {<Dropdown ui red search selection options={userOptions} defaultValue={r.assigned_reviewer_3} onChange={(event, { value }) => this.handleAssign("assigned_reviewer_3", value, r.id)} />}</h4>
                    </td>): (<td/>)}
                </tr>
            ) : (<p></p>)
        ));
        return resources_get
    }

    getDataUsers = (reviews, ids, currentReviewer) => {
        var usersData = [];
        for (var i = 0; i < this.state.users.length; i++) {
            usersData.push(
                {
                    id: this.state.users[i].id,
                    fName: this.state.users[i].first_name,
                    lName: this.state.users[i].last_name,
                    numApproved: 0,
                    numRejected: 0,
                    numPending: 0,
                    timeForAvg: 0,
                    countForAvg: 0,
                }
            )
        }


        this.state.resources.forEach(r => {
            if (r.assigned_reviewer != -1) {
                var indx = usersData.findIndex(x => x.id === r.assigned_reviewer);
                if (indx != -1) {
                    if (r.review_status === 'pending') {
                        usersData[indx].numPending++;
                    } else if (r.review_status === 'approved') {
                        usersData[indx].numApproved++;
                    } else if (r.review_status === 'rejected') {
                        usersData[indx].numRejected++;
                    }
                }
            }

            if (r.assigned_reviewer_2 != -1) {
                var indx = usersData.findIndex(x => x.id === r.assigned_reviewer_2);
                if (indx != -1) {
                    if (r.review_status_2 === 'pending') {
                        usersData[indx].numPending++;
                    } else if (r.review_status_2 === 'approved') {
                        usersData[indx].numApproved++;
                    } else if (r.review_status_2 === 'rejected') {
                        usersData[indx].numRejected++;
                    }
                }
            }
        });

        this.state.reviews.forEach(r => {
            if(r.review_time_sec != 0){
                var indx = usersData.findIndex(x => x.id === r.reviewer_user_email);
                if (indx != -1) {
                    usersData[indx].timeForAvg += r.review_time_sec;
                    usersData[indx].countForAvg ++;
                }
            }
        })

        const resources_get = usersData.map(usr =>
        (<tr key={usr.id} ref={tr => this.results = tr}>
            <td>
                <Popup content={usr.fName + ' ' + usr.lName} trigger={<p>{usr.lName}</p>} />
            </td>
            <td>
                <p>{(usr.timeForAvg)==0 ? '-' : (usr.timeForAvg/usr.countForAvg).toFixed(1)}</p>
            </td>
            <td class="positive">
                <h4>{usr.numApproved}</h4>
            </td>
            <td class="negative">
                <h4 >{usr.numRejected}</h4>
            </td>
            <td>
                <h4>{usr.numPending}</h4>
            </td>
        </tr>)
        );

        return resources_get
    }

    getUsersFooter = (reviews, ids, currentReviewer) => {
        var totalTime = 0;
        var totalTimeCount = 0;
        var totalApproved = 0;
        var totalRejected = 0;
        var totalPending = 0;
        
        this.state.resources.forEach(r => {
            if (r.assigned_reviewer != -1) {
                if (r.review_status === 'pending') {
                    totalPending++;
                } else if (r.review_status === 'approved') {
                    totalApproved++;
                } else if (r.review_status === 'rejected') {
                    totalRejected++;
                } else if (r.review_status === 'conflict') {
                    totalPending++;
                }
            }
            if (r.assigned_reviewer_2 != -1) {
                if (r.review_status_2 === 'pending') {
                    totalPending++;
                } else if (r.review_status_2 === 'approved') {
                    totalApproved++;
                } else if (r.review_status_2 === 'rejected') {
                    totalRejected++;
                } else if (r.review_status_2 === 'conflict') {
                    totalPending++;
                }
            }
        });

        this.state.reviews.forEach(r => {
            if(r.review_time_sec != 0){
                totalTime += r.review_time_sec;
                totalTimeCount ++;
            }
        });

        const resources_get = 
        (
        <tr ref={tr => this.results = tr}>
            <th>
                <strong>Total users</strong>
            </th>
            <th>
                <p>{(totalTime/totalTimeCount).toFixed(1)}</p>
            </th>
            <th class="positive">
                <p>{totalApproved}</p>
            </th>
            <th class="negative">
                <p>{totalRejected}</p>
            </th>
            <th>
                <p>{totalPending}</p>
            </th>
        </tr>
        );

        return resources_get
    }

    pendingHeader = () => {
        return <tr><th style={{ width: 250 }}>Resource</th><th style={{ width: 160 }}>Reviewer 1</th><th style={{ width: 160 }}>Reviewer 2</th><th style={{ width: 160 }}>Reviewer 3</th><th style={{ width: 160 }}>Reviewer 4</th><th style={{ width: 160 }}>Tiebreaker</th></tr>
    }
    usersHeader = () => {
        return <tr><th style={{ width: 350 }}>User</th><th>Avg t(s)</th><th>A</th><th>R</th><th>P</th></tr>
    }

    idToUserString = (idnum) => {
        if (idnum == -1) return "Unassigned";
        for (var i = 0; i < this.state.users.length; i++) {
            if (this.state.users[i].id == idnum) return this.state.users[i].first_name + " " + this.state.users[i].last_name
        }
    }

    resourceIsApproved = (resource) => {
        var numOfApprovals = 0
        if(resource.review_status_1_1 == 'approved')
            numOfApprovals +=1
        if(resource.review_status_2 == 'approved')
            numOfApprovals +=1
        if(resource.review_status_2_2 == 'approved')
            numOfApprovals +=1
        if(resource.review_status == 'approved')
            numOfApprovals +=1

        if (numOfApprovals>=2)
            return true
        return false
    }

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
        else if(resource.review_status_1_1 == 'reject')
            numOfRejects +=1
        
        if(resource.review_status_2 == 'approved')
            numOfApprovals +=1
        else if(resource.review_status_2 == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status_2 == 'reject')
            numOfRejects +=1

        if(resource.review_status_2_2 == 'approved')
            numOfApprovals +=1
        else if(resource.review_status_2_2 == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status_2_2 == 'reject')
            numOfRejects +=1

        if(resource.review_status == 'approved')
            numOfApprovals +=1
        else if(resource.review_status == 'conflict')
            numOfConflicts +=1
        else if(resource.review_status == 'reject')
            numOfRejects +=1

        if(numOfApprovals == numOfRejects && numOfApprovals>0)
            return true
        
        return false
    }

    render() {
        // Get current logged in user, take this function out of format_data and consolidate it later
        const reviewer = this.context.security.is_logged_in
            ? this.context.security.id
            : "Unknown user";

        const reviewsI = this.state.reviews.filter(review => review.reviewer_user_email === reviewer);
        var ids = []
        reviewsI.forEach(function (item) {
            ids.push(item.resource_id)
        })

        var reviewsApproval = new Map();
        reviewsI.forEach(function (item) {
            reviewsApproval.set(item.resource_id, [item.approved, item.review_comments, item.review_rating]);
        })

        const choices = [
            { text: 'most recent', value: 'newest' },
            { text: 'oldest', value: 'oldest' },
            { text: 'least reviewed', value: 'least reviewed' },
            { text: 'tie breaker needed', value: 'tie breakers' },
            { text: 'conflict of interests', value: 'conflict' },
        ]

        const { value } = this.state.order;
        return (
            <div>
                <div style={{ paddingTop: '2%', paddingLeft: '6%', paddingRight: '6%' }}>
                    <div style={{ padding: "2em 0em", textAlign: "center" }}
                        vertical>
                    </div>
                    {this.state.pending === 'Completed Reviews' ?
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
                        : null}
                    <Grid celled>
                        <Grid.Row>
                            <Grid.Column width={5}>
                                <div style={{ height: '500px', overflowX: "scroll", width: "100%" }}>
                                    <Table class="ui definition table">
                                        <thead>
                                            {this.usersHeader()}
                                        </thead>
                                        <tbody>
                                            {this.getDataUsers(this.state.reviews, ids, reviewer)}
                                        </tbody>
                                        <tfoot>
                                            {this.getUsersFooter()}
                                        </tfoot>
                                    </Table>
                                </div>
                            </Grid.Column>
                            <Grid.Column width={11}>
                                <div style={{ height: '500px', overflowX: "scroll", width: "100%" }}>
                                    <Table class="ui celled table">
                                        <thead>
                                            {this.pendingHeader()}
                                        </thead>
                                        <tbody>
                                            {this.getData(this.state.reviews, ids, reviewer)}
                                        </tbody>
                                    </Table>
                                </div>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </div>
            </div>
        );
    }
}