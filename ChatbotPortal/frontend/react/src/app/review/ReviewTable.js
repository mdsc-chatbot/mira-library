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
import { Table, Header, Rating, Dropdown, Checkbox } from "semantic-ui-react";
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
            pending: 'Completed Reviews',
            header:'Review new resources and tags here!',
            resourceData:{},
            order:"newest",
            assignedOnly: true
        };
    }

    get_resources = () => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/resource", {headers: options}).then(res => {
            this.setState({
                resources: res.data
            });
        });
    };

    get_reviews = () =>{
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/api/review", {headers: options}).then(res => {
            this.setState({
                reviews: res.data
            });
        });
    }

    componentDidMount() {
        this.get_resources();
        this.get_reviews();
    }


    completedReviews = (ids, reviews) => {
        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            ids.includes(r.id) === true ?(
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>{reviews.get(r.id)[1]}</td>
                    <td><Rating
                                icon="star"
                                defaultRating={reviews.get(r.id)[2]}
                                maxRating={5}
                                disabled
                                size="massive"/>
                    </td>
                    <td>
                        {reviews.get(r.id)[0]===true?(<i class="check icon"></i>):(<i class="x icon"></i>)}
                    </td>
                </tr>
            ):(<p></p>)
        ));
        return resources_get

    }
    
    switchView = () =>{
        if (this.state.pending === 'Completed Reviews'){
            this.setState({pending:'Pending Reviews',header:'View a list of your review actions here!'});
        } else {
            this.setState({pending:'Completed Reviews',header:'Review new resources and tags here!'})
        }
    }

    handleOrder = (e, {value}) => {this.setState({ order: {value}.value})}

    
    getData = (reviews,ids,currentReviewer) =>{
        function numRevs(id){var numReviews = reviews.reduce(function (n, reviews) {
            return n + (reviews.resource_id == id);
        }, 0); return numReviews}
        function numRevsApproved(id){var numReviews = reviews.reduce(function (n, reviews) {
            return n + (reviews.resource_id == id && reviews.approved === true);
        }, 0); return numReviews}
        function numRevsRejected(id){var numReviews = reviews.reduce(function (n, reviews) {
            return n + (reviews.resource_id == id && reviews.approved === false);
        }, 0); return numReviews}
        function compareOldest( a, b ) {
            if ((new Date(a.timestamp).getTime()/1000) < (new Date(b.timestamp).getTime()/1000)){
              return -1;
            }
            if ( (new Date(a.timestamp).getTime()/1000) > (new Date(b.timestamp).getTime()/1000) ){
              return 1;
            }
            return 0;
          }
          function compareNewest( a, b ) {
            if ((new Date(a.timestamp).getTime()/1000) > (new Date(b.timestamp).getTime()/1000)){
              return -1;
            }
            if ( (new Date(a.timestamp).getTime()/1000) < (new Date(b.timestamp).getTime()/1000) ){
              return 1;
            }
            return 0;
          }
          function compareReviews( a, b) {
              if(numRevs(a.id) < numRevs(b.id)){
                  return -1;
              }
              if(numRevs(a.id) > numRevs(b.id)){
                return 1;
              }
              return 0;
          }
          function compareTieBreak( a){
            if(numRevsApproved(a.id) > 0 && numRevsApproved(a.id) === numRevsRejected(a.id)){
                console.log(a.id)
                return -1;
            }
            if(numRevsApproved(a.id) > 0 && numRevsApproved(a.id) !== numRevsRejected(a.id)){
                return 0;
            }
            return 1;
            //console.log(a.id,numRevsApproved(a.id))
          }

        if (this.state.order === 'oldest'){
            this.state.resources = this.state.resources.sort(compareOldest)
        }else if(this.state.order === 'newest'){
            this.state.resources = this.state.resources.sort(compareNewest)
        }else if(this.state.order === 'least reviewed'){
            this.state.resources = this.state.resources.sort(compareReviews)
        }else if(this.state.order === 'tie breakers'){
            this.state.resources = this.state.resources.sort(compareTieBreak)
        }
        console.log(this.state.order,this.state.resources)

        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            ids.includes(r.id) !== true && r.created_by_user_pk !== currentReviewer 
            && ((r.assigned_reviewer === currentReviewer || r.assigned_reviewer_2 === currentReviewer) || (!this.state.assignedOnly && (r.assigned_reviewer === -1 || r.assigned_reviewer_2 === -1))) ?(
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>
                        <button class="right floated ui button"><Link to={baseRoute + "/review/"+r.id}>Review</Link></button>
                    </td>
                </tr>
            ):(<p></p>)
        ));
        console.log(resources_get)
        return resources_get
    }
    pendingHeader = () =>{
        return <tr><th>Resource</th><th></th></tr>
    }
    completedHeader = () =>{
        return <tr><th>Resource</th><th>Review Comments</th><th>Review Rating</th><th></th></tr>
    }

    sorting = (options) =>{
        return <tr><th>Resource</th><th>Review Comments</th><th>Review Rating</th><th></th></tr>
    }
    render() {    
        // Get current logged in user, take this function out of format_data and consolidate it later
        const reviewer = this.context.security.is_logged_in
        ? this.context.security.id
        : "Unknown user";

        const reviewsI = this.state.reviews.filter(review => review.reviewer_user_email === reviewer);
        var ids = []
        reviewsI.forEach(function (item){
            ids.push(item.resource_id)
        })

        var reviewsApproval = new Map();
        reviewsI.forEach(function (item){
            reviewsApproval.set(item.resource_id, [item.approved, item.review_comments, item.review_rating]);
        })

        const choices= [
            {text:'most recent', value: 'newest'},
            {text:'oldest', value: 'oldest'},
            {text:'least reviewed', value: 'least reviewed'},
            {text:'tie breaker needed', value:'tie breakers'}
          ]

        const { value } = this.state.order;
        const resources = this.state.resources
        var viewPending = true
        return (
            <div>
                <div style={{paddingTop:'2%', paddingLeft:'6%', paddingRight:'6%'}}>
                    <div style={{ padding: "2em 0em",textAlign: "center" }}
                        vertical>
                    </div>
                    {this.state.pending === 'Completed Reviews'?
                        <div style={{display:'inline-block'}}>
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
                    :null}
                    <button class="ui right floated button" style={{display:'inline'}} onClick={() => this.switchView()}>{this.state.pending}</button> 
                    <Checkbox onChange={()=>this.setState((prevState) => ({ assignedOnly: !prevState.assignedOnly }))} checked={this.state.assignedOnly} label="Assigned Resources Only"/>
                    <div style={{height: '500px',overflowX: "scroll", width:"100%"}}>
                        <Table class="ui celled table">
                            <thead>
                                {this.state.pending === 'Completed Reviews'?(this.pendingHeader()):(this.completedHeader())}
                            </thead>
                            <tbody>
                                {this.state.pending === 'Completed Reviews'?(this.getData(this.state.reviews,ids,reviewer)):(this.completedReviews(ids, reviewsApproval))}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </div>
        );
    }
}