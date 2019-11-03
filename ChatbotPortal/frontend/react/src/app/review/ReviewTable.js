import React, { Component } from "react";
import axios from "axios";
import { Table, Header, Rating, Dropdown } from "semantic-ui-react";
import { SecurityContext } from "../security/SecurityContext";
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
        order:"most recent"
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

    
    getData = (ids) =>{
        function compare( a, b ) {
            if ((new Date(a.timestamp).getTime()/1000) < (new Date(b.timestamp).getTime()/1000)){
              return -1;
            }
            if ( (new Date(a.timestamp).getTime()/1000) > (new Date(b.timestamp).getTime()/1000) ){
              return 1;
            }
            return 0;
          }
          function compare2( a, b ) {
            if ((new Date(a.timestamp).getTime()/1000) > (new Date(b.timestamp).getTime()/1000)){
              return -1;
            }
            if ( (new Date(a.timestamp).getTime()/1000) < (new Date(b.timestamp).getTime()/1000) ){
              return 1;
            }
            return 0;
          }

        if (this.state.order === 'oldest'){
            this.state.resources = this.state.resources.sort(compare)
        }else if(this.state.order ==='most recent'){
            this.state.resources = this.state.resources.sort(compare2)
        }
        console.log(this.state.order,this.state.resources)

        const resources_get = this.state.resources.length > 0 && this.state.resources.map(r => (
            ids.includes(r.id) !== true ?(
                <tr key={r.id} ref={tr => this.results = tr}>
                    <td><Link to={baseRoute + "/resource/" + r.id}>{r.title}</Link></td>
                    <td>{r.id}</td>
                    <td>{r.timestamp}</td>
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

        var reviewsApproval = new Map();
        reviewsI.forEach(function (item){
            reviewsApproval.set(item.resource_id, [item.approved, item.review_comments, item.review_rating]);
        })

        const choices= [
            {text:'most recent', value: 'most recent'},
            {text:'oldest', value: 'oldest'},
            {text:'least reviewed', value: 'least reviewed'},
            {text:'tie breaker needed', value:'tie breakers'}
          ]

        const { value } = this.state.order;
        const resources = this.state.resources
        var viewPending = true
        return (
            <div>
                <div style={{paddingTop:30, paddingLeft:100, paddingRight:100}}>
                    <div style={{ padding: "2em 0em",textAlign: "center" }}
                        vertical>

                        <Header
                            as="h3"
                            style={{
                                fontSize: "2em"
                            }}
                            color="blue">
                            Reviews
                        </Header>

                        <Header as="h4" color="grey">{this.state.header}</Header>
                    </div>
                    <h4>Order Submissions By </h4>
                    <Dropdown class="ui inline dropdown"
                        name="subject"
                        placeholder='most recent'
                        selection 
                        onChange={this.handleOrder}
                        options={choices} 
                        value={value}
                    />
                    <button class="ui right floated button" style={{display:"block"}} onClick={() => this.switchView()}>{this.state.pending}</button>
                    <div style={{height: '500px',overflowX: "scroll", width:"100%"}}>
                        <Table class="ui celled table">
                            <thead>
                                {this.state.pending === 'Completed Reviews'?(this.pendingHeader()):(this.completedHeader())}
                            </thead>
                            <tbody>
                                {this.state.pending === 'Completed Reviews'?(this.getData(ids)):(this.completedReviews(ids, reviewsApproval))}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </div>
        );
    }
}