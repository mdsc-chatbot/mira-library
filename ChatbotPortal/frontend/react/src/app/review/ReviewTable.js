import React, { Component } from "react";
import axios from "axios";
import { Table, List } from "semantic-ui-react";
import { SecurityContext } from "../security/SecurityContext";
import { baseRoute } from "../App";
import { Link } from "react-router-dom";

export default class ReviewTable extends Component {
    static contextType = SecurityContext;
    
    constructor(props) {
        super(props);
        this.state = {
        resources: {},
        reviews: [],
        pending: 'Completed Reviews'
        };
    }

    get_resources = () => {
        axios.get("http://127.0.0.1:8000/api/resource").then(res => {
            this.setState({
                resources: res.data
            });
        });
    };

    get_reviews = () =>{
        axios.get("http://127.0.0.1:8000/api/review").then(res => {
            this.setState({
                reviews: res.data
            });
        });
    }
    componentDidMount() {
        this.get_resources();
        this.get_reviews();
    }

    format_data = (data, approval) => {
        // Get current logged in user
        const reviewer = this.context.security.email
            ? this.context.security.email
            : "Unknown user";

        const formatted_review = {
            reviewer_user_email: reviewer,
            approved: approval,
            resource_url: data.url,
            resource_id: data.id
        };
        return formatted_review;
    };

    completedReviews = (ids, reviews) => {
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            ids.includes(r.id) === true ?(
                console.log(r.id),
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>{r.comments}</td>
                    <td>filler tags</td>
                    {/*<td>{r.tags}</td> this is more complicated than just grabbing them*/}
                    <td>
                        {reviews.get(r.id)===true?(<i class="check icon"></i>):(<i class="x icon"></i>)}
                    </td>
                </tr>
            ):(<p></p>)
        ));
        return resources_get

    }
    switchView = () =>{
        if (this.state.pending === 'Completed Reviews'){
            this.setState({pending:'Pending Reviews'});
        } else {
            this.setState({pending:'Completed Reviews'})
        }
    }

    approve = (data) => {
        const review = this.format_data(data, true);
        console.log(review)
        axios
            .post("http://127.0.0.1:8000/api/review/", review)
            .then(res => {})
            .catch(error => console.error(error));
        this.get_reviews();
    };

    reject = (data) => {
        const review = this.format_data(data, false);
        console.log(review)
        axios
            .post("http://127.0.0.1:8000/api/review/", review)
            .then(res => {})
            .catch(error => console.error(error));
        this.get_reviews();
    }

    getData = (ids) =>{
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            ids.includes(r.id) !== true ?(
                console.log(r.id),
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>{r.comments}</td>
                    <td>filler tags</td>
                    {/*<td>{r.tags}</td> this is more complicated than just grabbing them*/}
                    <td>
                        <button class="positive ui button" onClick={() => this.approve(r)}>Approve</button>
                        <button class="negative ui button" onClick={() => this.reject(r)}>Reject</button>
                    </td>
                </tr>
            ):(<p></p>)
        ));
        return resources_get
    }

    render() {    
        // Get current logged in user, take this function out of format_data and consolidate it later
        const reviewer = this.context.security.email
        ? this.context.security.email
        : "Unknown user";

        const reviewsI = this.state.reviews.filter(review => review.reviewer_user_email === reviewer);
        var ids = []
        reviewsI.forEach(function (item){
            ids.push(item.resource_id)
        })
        console.log("rev",ids)

        var reviewsApproval = new Map();
        reviewsI.forEach(function (item){
            reviewsApproval.set(item.resource_id, item.approved);
        })

        const resources = this.state.resources
        console.log("waow",resources);
        var viewPending = true
        return (
            <div>
                <div style={{paddingTop:30, paddingLeft:100, paddingRight:100}}>
                    Reviews
                    <button class="ui right floated button" onClick={() => this.switchView()}>{this.state.pending}</button>
                    <Table class="ui celled table">
                        <thead>
                            <tr>
                            <th>URL</th>
                            <th>Comments</th>
                            <th>Tags</th>
                            <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.pending === 'Completed Reviews'?(this.getData(ids)):(this.completedReviews(ids, reviewsApproval))}
                        </tbody>
                    </Table>
                </div>
            </div>
        );
    }
}