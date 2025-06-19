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
import { Table, Popup, Dropdown, Grid, Input, Checkbox, Loader, Pagination } from "semantic-ui-react";
import { SecurityContext } from "../contexts/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";
import ReviewPopover from "../review/ReviewPopover"

const ITEMS_PER_PAGE = 10;

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
            order: "newest",
            searchTerm: "",
            hideApprovedRejected: false,
            loading: true,
            currentPage: 1,
            cachedUserStats: null,
            cachedTotalStats: null
        };

        // Bind methods
        this.filterResources = this.filterResources.bind(this);
        this.resourceIsApproved = this.resourceIsApproved.bind(this);
        this.resourceNeedTieBreaker = this.resourceNeedTieBreaker.bind(this);
    }

    resourceNeedTieBreaker(resource) {
        if(resource.assigned_reviewer_3 !== -1) return false;

        const statuses = [
            resource.review_status_1_1,
            resource.review_status_2,
            resource.review_status_2_2,
            resource.review_status
        ];

        const numOfApprovals = statuses.filter(status => status === 'approved').length;
        const numOfRejects = statuses.filter(status => status === 'rejected').length;

        return numOfApprovals === numOfRejects && numOfApprovals > 0;
    }

    get_resources = async () => {
        this.setState({ loading: true });
        try {
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };
            const res = await axios.get("/chatbotportal/resource", { headers: options });
            this.setState({ resources: res.data });
        } catch (error) {
            console.error("Error fetching resources:", error);
        }
        this.setState({ loading: false });
    };

    get_reviews = async () => {
        try {
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };
            const res = await axios.get("/api/review", { headers: options });
            this.setState({ reviews: res.data });
        } catch (error) {
            console.error("Error fetching reviews:", error);
        }
    }

    get_users = async () => {
        try {
            const options = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.context.security.token}`
            };
            const res = await axios.get("/chatbotportal/authentication/super/search/status/1/1/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search=&page_size=100", { headers: options });
            this.setState({ users: res.data.results });
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    }

    async componentDidMount() {
        await Promise.all([
            this.get_resources(),
            this.get_reviews(),
            this.get_users()
        ]);
    }

    handleOrder = (e, { value }) => { 
        this.setState({ 
            order: value,
            currentPage: 1,
            cachedUserStats: null,
            cachedTotalStats: null
        }); 
    }

    handleSearch = (e, { value }) => { 
        this.setState({ 
            searchTerm: value,
            currentPage: 1,
            cachedUserStats: null,
            cachedTotalStats: null
        }); 
    }

    handleHideApprovedRejected = (e, { checked }) => { 
        this.setState({ 
            hideApprovedRejected: checked,
            currentPage: 1,
            cachedUserStats: null,
            cachedTotalStats: null
        }); 
    }

    handlePageChange = (e, { activePage }) => {
        this.setState({ currentPage: activePage });
    }

    handleAssign = (field, value, rid) => {
        const submitCmd = { [field]: value };

        const options = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.context.security.token}`
        };

        axios.put(
            "/chatbotportal/resource/" + rid + "/updatepartial/",
            submitCmd,
            { headers: options }
        ).catch(error => {
            console.error("Error updating assignment:", error);
        });
    }

    sortResources = (resources) => {
        const sortFunctions = {
            'oldest': (a, b) => new Date(a.timestamp) - new Date(b.timestamp),
            'newest': (a, b) => new Date(b.timestamp) - new Date(a.timestamp),
            'least reviewed': (a, b) => {
                const getReviewCount = (r) => [r.review_status, r.review_status_2, r.review_status_1_1, r.review_status_2_2]
                    .filter(s => s !== 'pending').length;
                return getReviewCount(a) - getReviewCount(b);
            },
            'tie breakers': (a, b) => this.resourceNeedTieBreaker(a) ? -1 : 1,
            'conflict': (a, b) => {
                const hasConflict = r => ['review_status', 'review_status_2', 'review_status_1_1', 'review_status_2_2']
                    .some(field => r[field] === 'conflict');
                return hasConflict(a) ? -1 : hasConflict(b) ? 1 : 0;
            }
        };

        return [...resources].sort(sortFunctions[this.state.order] || sortFunctions.newest);
    }

    filterResources(resources) {
        return resources.filter(r => {
            const matchesSearch = r.title.toLowerCase().includes(this.state.searchTerm.toLowerCase());
            const isApprovedOrRejected = this.resourceIsApproved(r) || this.resourceIsRejected(r);
            return matchesSearch && (!this.state.hideApprovedRejected || !isApprovedOrRejected);
        });
    }

    calculateUserStats() {
        if (this.state.cachedUserStats) return this.state.cachedUserStats;

        const stats = this.state.users.map(user => {
            const userData = {
                id: user.id,
                fName: user.first_name,
                lName: user.last_name,
                numApproved: 0,
                numRejected: 0,
                numPending: 0,
                timeForAvg: 0,
                countForAvg: 0,
            };

            this.state.resources.forEach(r => {
                ['assigned_reviewer', 'assigned_reviewer_2', 'assigned_reviewer_1_1', 'assigned_reviewer_2_2'].forEach(field => {
                    if (r[field] === user.id) {
                        const status = r[field === 'assigned_reviewer' ? 'review_status' : 
                                       field === 'assigned_reviewer_2' ? 'review_status_2' :
                                       field === 'assigned_reviewer_1_1' ? 'review_status_1_1' : 'review_status_2_2'];
                        
                        if (status === 'pending') userData.numPending++;
                        else if (status === 'approved') userData.numApproved++;
                        else if (status === 'rejected') userData.numRejected++;
                    }
                });
            });

            this.state.reviews.forEach(r => {
                if (r.review_time_sec !== 0 && r.reviewer_user_email === user.id) {
                    userData.timeForAvg += r.review_time_sec;
                    userData.countForAvg++;
                }
            });

            return userData;
        });

        this.setState({ cachedUserStats: stats });
        return stats;
    }

    resourceIsApproved(resource) {
        const approvedStatuses = [
            resource.review_status_1_1,
            resource.review_status_2,
            resource.review_status_2_2,
            resource.review_status
        ].filter(status => status === 'approved');

        return approvedStatuses.length >= 2;
    }

    resourceIsRejected(resource) {
        const rejectedStatuses = [
            resource.review_status_1_1,
            resource.review_status_2,
            resource.review_status_2_2,
            resource.review_status
        ].filter(status => status === 'rejected');

        return rejectedStatuses.length >= 2;
    }

    render() {
        if (this.state.loading) {
            return <Loader active>Loading...</Loader>;
        }

        const reviewer = this.context.security.is_logged_in ? this.context.security.id : "Unknown user";
        
        // Filter and sort resources
        const filteredResources = this.filterResources(this.state.resources);
        const sortedResources = this.sortResources(filteredResources);

        // Pagination
        const totalPages = Math.ceil(sortedResources.length / ITEMS_PER_PAGE);
        const startIndex = (this.state.currentPage - 1) * ITEMS_PER_PAGE;
        const paginatedResources = sortedResources.slice(startIndex, startIndex + ITEMS_PER_PAGE);

        // Calculate user stats
        const userStats = this.calculateUserStats();

        const choices = [
            { text: 'most recent', value: 'newest' },
            { text: 'oldest', value: 'oldest' },
            { text: 'least reviewed', value: 'least reviewed' },
            { text: 'tie breaker needed', value: 'tie breakers' },
            { text: 'conflict of interests', value: 'conflict' },
        ];

        // Map users for assignment dropdown
        const userOptions = this.state.users.map(user => ({
            key: user.id,
            value: user.id,
            text: `${user.first_name} ${user.last_name}`
        })).concat([{ key: -1, value: -1, text: "Unassigned" }]);

        return (
            <div>
                <div style={{ paddingTop: '2%', paddingLeft: '6%', paddingRight: '6%' }}>
                    <Grid verticalAlign="middle">
                        <Grid.Row columns={3} style={{ alignItems: 'center' }}>
                            <Grid.Column>
                                {this.state.pending === 'Completed Reviews' && (
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                        <h4 style={{ margin: 0 }}>Order Submissions By </h4>
                                        <Dropdown
                                            style={{ minHeight: '38px' }}
                                            className="ui dropdown"
                                            name="subject"
                                            placeholder='most recent'
                                            selection
                                            onChange={this.handleOrder}
                                            options={choices}
                                            value={this.state.order}
                                        />
                                    </div>
                                )}
                            </Grid.Column>
                            <Grid.Column textAlign="center">
                                <Input
                                    icon='search'
                                    placeholder='Search by title...'
                                    onChange={this.handleSearch}
                                    value={this.state.searchTerm}
                                    style={{ width: '100%', maxWidth: '400px' }}
                                />
                            </Grid.Column>
                            <Grid.Column textAlign="right">
                                <Checkbox
                                    label='Hide Approved/Rejected Resources'
                                    onChange={this.handleHideApprovedRejected}
                                    checked={this.state.hideApprovedRejected}
                                    style={{ marginRight: '20px' }}
                                />
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>

                    <Grid celled>
                        <Grid.Row>
                            <Grid.Column width={5}>
                                <div style={{ height: '500px', overflowX: "scroll", width: "100%" }}>
                                    <Table className="ui definition table">
                                        <thead>
                                            <tr>
                                                <th style={{ width: 350 }}>User</th>
                                                <th>Avg t(s)</th>
                                                <th>A</th>
                                                <th>R</th>
                                                <th>P</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {userStats.map(usr => (
                                                <tr key={usr.id}>
                                                    <td>
                                                        <Popup 
                                                            content={`${usr.fName} ${usr.lName}`} 
                                                            trigger={<p>{usr.lName}</p>} 
                                                        />
                                                    </td>
                                                    <td>
                                                        <p>{usr.countForAvg === 0 ? '-' : (usr.timeForAvg/usr.countForAvg).toFixed(1)}</p>
                                                    </td>
                                                    <td className="positive">
                                                        <h4>{usr.numApproved}</h4>
                                                    </td>
                                                    <td className="negative">
                                                        <h4>{usr.numRejected}</h4>
                                                    </td>
                                                    <td>
                                                        <h4>{usr.numPending}</h4>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                </div>
                            </Grid.Column>
                            <Grid.Column width={11}>
                                <div style={{ height: '500px', overflowX: "scroll", width: "100%" }}>
                                    <Table className="ui celled table">
                                        <thead>
                                            <tr>
                                                <th style={{ width: 250 }}>Resource</th>
                                                <th style={{ width: 160 }}>Reviewer 1</th>
                                                <th style={{ width: 160 }}>Reviewer 2</th>
                                                <th style={{ width: 160 }}>Reviewer 3</th>
                                                <th style={{ width: 160 }}>Reviewer 4</th>
                                                <th style={{ width: 160 }}>Tiebreaker</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {paginatedResources.map(r => (
                                                <tr key={r.id}>
                                                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                                                    <td>
                                                        <h4>
                                                            {r.review_status === "approved" ? 
                                                                <p><i className="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer}/></p> : 
                                                             r.review_status === "pending" ? 
                                                                <p><i className="x icon"></i> pending</p> : 
                                                             r.review_status === "conflict" ? 
                                                                <p><i className="red stop circle outline icon"></i>Conflict of Interest</p> : 
                                                                <p><i className="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer}/></p>}
                                                            <Dropdown 
                                                                selection 
                                                                options={userOptions} 
                                                                defaultValue={r.assigned_reviewer} 
                                                                onChange={(e, { value }) => this.handleAssign("assigned_reviewer", value, r.id)}
                                                            />
                                                        </h4>
                                                    </td>
                                                    <td>
                                                        <h4>
                                                            {r.review_status_2 === "approved" ? 
                                                                <p><i className="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2}/></p> : 
                                                             r.review_status_2 === "pending" ? 
                                                                <p><i className="x icon"></i> pending</p> : 
                                                             r.review_status_2 === "conflict" ? 
                                                                <p><i className="red stop circle outline icon"></i>Conflict of Interest</p> : 
                                                                <p><i className="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2}/></p>}
                                                            <Dropdown 
                                                                selection 
                                                                options={userOptions} 
                                                                defaultValue={r.assigned_reviewer_2} 
                                                                onChange={(e, { value }) => this.handleAssign("assigned_reviewer_2", value, r.id)}
                                                            />
                                                        </h4>
                                                    </td>
                                                    <td>
                                                        <h4>
                                                            {r.review_status_1_1 === "approved" ? 
                                                                <p><i className="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_1_1}/></p> : 
                                                             r.review_status_1_1 === "pending" ? 
                                                                <p><i className="x icon"></i> pending</p> : 
                                                             r.review_status_1_1 === "conflict" ? 
                                                                <p><i className="red stop circle outline icon"></i>Conflict of Interest</p> : 
                                                                <p><i className="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_1_1}/></p>}
                                                            <Dropdown 
                                                                selection 
                                                                options={userOptions} 
                                                                defaultValue={r.assigned_reviewer_1_1} 
                                                                onChange={(e, { value }) => this.handleAssign("assigned_reviewer_1_1", value, r.id)}
                                                            />
                                                        </h4>
                                                    </td>
                                                    <td>
                                                        <h4>
                                                            {r.review_status_2_2 === "approved" ? 
                                                                <p><i className="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2_2}/></p> : 
                                                             r.review_status_2_2 === "pending" ? 
                                                                <p><i className="x icon"></i> pending</p> : 
                                                             r.review_status_2_2 === "conflict" ? 
                                                                <p><i className="red stop circle outline icon"></i>Conflict of Interest</p> : 
                                                                <p><i className="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_2_2}/></p>}
                                                            <Dropdown 
                                                                selection 
                                                                options={userOptions} 
                                                                defaultValue={r.assigned_reviewer_2_2} 
                                                                onChange={(e, { value }) => this.handleAssign("assigned_reviewer_2_2", value, r.id)}
                                                            />
                                                        </h4>
                                                    </td>
                                                    {this.resourceNeedTieBreaker(r) ? (
                                                        <td>
                                                            <h4>
                                                                {r.review_status_3 === "approved" ? 
                                                                    <p><i className="green check icon"></i> approved <ReviewPopover resId={r.id} revId={r.assigned_reviewer_3}/></p> : 
                                                                 r.review_status_3 === "pending" ? 
                                                                    <p><i className="x icon"></i> pending</p> : 
                                                                 r.review_status_3 === "conflict" ? 
                                                                    <p><i className="red stop circle outline icon"></i>Conflict of Interest</p> : 
                                                                    <p><i className="red x icon"></i> rejected <ReviewPopover resId={r.id} revId={r.assigned_reviewer_3}/></p>}
                                                                <Dropdown 
                                                                    selection 
                                                                    options={userOptions} 
                                                                    defaultValue={r.assigned_reviewer_3} 
                                                                    onChange={(e, { value }) => this.handleAssign("assigned_reviewer_3", value, r.id)}
                                                                />
                                                            </h4>
                                                        </td>
                                                    ) : <td/>}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                </div>
                                <div style={{ marginTop: '1em', textAlign: 'center' }}>
                                    <Pagination
                                        activePage={this.state.currentPage}
                                        onPageChange={this.handlePageChange}
                                        totalPages={totalPages}
                                        ellipsisItem={null}
                                    />
                                </div>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </div>
            </div>
        );
    }
}
