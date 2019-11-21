import React, {Component} from "react";
import axios from "axios";
import {Container, Divider, Form, Header, Icon, Label, Rating} from "semantic-ui-react";
import {SecurityContext} from "../security/SecurityContext";
import {baseRoute} from "../App";
import {Link} from "react-router-dom";

export default class ResourceDetail extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);

        this.state = {
            resource: {},
            rating: 1,
            comments: "No comments",
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
    }

    approve = data => {
        const review = this.format_data(data, true);
        console.log(review);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("http://127.0.0.1:8000/api/review/", review, {headers: options})
            .then(res => {
            })
            .catch(error => console.error(error));
        this.update_resource_user("approved");
    };

    reject = data => {
        const review = this.format_data(data, false);
        console.log(review);
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .post("http://127.0.0.1:8000/api/review/", review, {headers: options})
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
                    {"review_status": review_status},
                    {headers: options}
                )
                .then(
                    response => {
                    },
                    error => {
                        console.log(error);
                    }
                );

            // User
            console.log(this.state.resource);
            console.log(review_status);
            if (review_status === "approved") {
                axios
                    .put(`/chatbotportal/authentication/${this.context.security.id}/update/approved_submissions/`, {
                        headers: { Authorization: `Bearer ${this.context.security.token}` }
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
                                        <Header as="h3" style={{fontSize: "2em"}}>
                                            <Icon name="globe"/>
                                            <Header.Content>
                                                {this.state.resource.title}
                                            </Header.Content>
                                        </Header>

                                        <Divider></Divider>

                                        <p style={{color: "grey", paddingTop: 25}}>
                                            Submitted by {this.state.resource.created_by_user}
                                        </p>
                                        <p style={{color: "grey", marginTop: -10}}>
                                            Date submitted: {this.state.resource.timestamp}
                                        </p>

                                        <a href={this.state.resource.url} target="_blank">
                                            <h4>{this.state.resource.url}</h4>
                                        </a>

                                        {this.state.resource.rating ? (
                                            <p>
                                                <Rating
                                                    icon="star"
                                                    defaultRating={this.state.resource.rating}
                                                    maxRating={5}
                                                    disabled
                                                    size="massive"
                                                />
                                            </p>
                                        ) : null}
                                        {this.state.resource.tags &&
                                        this.state.resource.tags.length > 0 ? (
                                            <p>
                                                <span style={{color: "grey"}}>Tags:</span>
                                                {this.state.resource.tags.map(tag => (
                                                    <Label key={tag} size="large">
                                                        {tag}
                                                    </Label>
                                                ))}
                                            </p>
                                        ) : null}
                                        {this.state.resource.attachment ? (
                                            <Header as="h5" color="grey">
                                                <a href="#" onClick={this.downloadAttachment}>
                                                    <Icon name="download"/>
                                                    <Header.Content>
                                                        Download attachment
                                                    </Header.Content>
                                                </a>
                                            </Header>
                                        ) : null}
                                        <Header as="h5" color="grey">
                                            <Icon name="comment"/>
                                            <Header.Content>Comments:</Header.Content>
                                        </Header>
                                        <p style={{color: "grey", marginTop: -10}}>
                                            {this.state.resource.comments}
                                        </p>
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
                                            {console.log(this.state.resource)}
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
