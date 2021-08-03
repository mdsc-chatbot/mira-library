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
 import { Table, Header, Rating, Dropdown } from "semantic-ui-react";
 import { SecurityContext } from "../contexts/SecurityContext";
 import { baseRoute } from "../App";
 import { Link } from "react-router-dom";
 
 
 export default class ManageReviews extends Component {
     static contextType = SecurityContext;
     
     constructor(props) {
         super(props);
         this.state = {
         resources: [],
         reviews: [],
         users: [],
         pending: 'Completed Reviews',
         header:'Review new resources and tags here!',
         resourceData:{},
         order:"newest"
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

     get_users = () =>{
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios.get("/chatbotportal/authentication/super/search/status/''/''/''/''/''/date_range/''/''/''/id_range/''/''/submission_range/''/''/''/search_value/?search=", {headers: options}).then(res => {
            this.setState({
                users: res.data.results
            });
        });
    }
 
     componentDidMount() {
         this.get_resources();
         this.get_reviews();
         this.get_users();
     }
 
 
     handleOrder = (e, {value}) => {this.setState({ order: {value}.value})}
 
     handleAssign = (field, value, rid) =>
     {
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
                 //console.log(a.id)
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

         //map users for assignment dropdown
         var userOptions = [];
         for(var i = 0; i < this.state.users.length; i++)
         {
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
             r.review_status !== "approved" || r.review_status_2 !== "approved" ?(
                 <tr key={r.id} ref={tr => this.results = tr}>
                     <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                     <td>
                         <h4><Dropdown options={userOptions} defaultValue={r.assigned_reviewer} onChange={(event, {value})=>this.handleAssign("assigned_reviewer", value, r.id)}/></h4>
                     </td>
                     <td>
                        <h4>{<Dropdown options={userOptions} defaultValue={r.assigned_reviewer_2} onChange={(event,  {value})=>this.handleAssign("assigned_reviewer_2", value, r.id)}></Dropdown>}</h4>
                     </td>
                 </tr>
             ):(<p></p>)
         ));
         //console.log(resources_get)
         return resources_get
     }
     pendingHeader = () =>{
         return <tr><th style={{width: 300}}>Resource</th><th style={{width: 200}}>Reviewer One</th><th style={{width: 200}}>Reviewer Two</th></tr>
     }

     idToUserString = (idnum) =>
     {
         if(idnum == -1) return "Unassigned";
         for(var i = 0; i < this.state.users.length; i++)
         {
            if(this.state.users[i].id == idnum) return this.state.users[i].first_name + " " + this.state.users[i].last_name
         }
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
                     <div style={{height: '500px',overflowX: "scroll", width:"100%"}}>
                         <Table class="ui celled table">
                             <thead>
                                 {this.pendingHeader()}
                             </thead>
                             <tbody>
                                 {this.getData(this.state.reviews,ids,reviewer)}
                             </tbody>
                         </Table>
                     </div>
                 </div>
             </div>
         );
     }
 }