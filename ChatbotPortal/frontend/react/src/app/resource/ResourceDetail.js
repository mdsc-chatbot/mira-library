import React, { Component } from "react";
import axios from "axios";
import {
    Header,
    Icon,
    Rating,
    Popup,
    Card,
    Container,
    Divider
} from "semantic-ui-react";

import styles from "./Resource.css";

export default class ResourceDetail extends Component {
    constructor(props) {
        super(props);

        this.state = {
            resource: {}
        };
    }

    componentDidMount() {
        const resourceID = this.props.match.params.resourceID;
        axios
            .get(`http://127.0.0.1:8000/api/resource/${resourceID}`)
            .then(res => {
                this.setState({
                    resource: res.data
                });
            });
    }

    render() {
        return (
            <div
                style={{ paddingTop: 30, paddingLeft: 100, paddingRight: 100 }}
            >
                <Container>
                    <Header as="h3" style={{ fontSize: "2em" }}>
                        <Icon name="globe" />
                        <Header.Content>
                            {this.state.resource.title}
                        </Header.Content>
                    </Header>

                    <Divider></Divider>

                    <p style={{ color: "grey", paddingTop: 25 }}>
                        Submitted by {this.state.resource.created_by_user}
                    </p>
                    <p style={{ color: "grey", marginTop: -10 }}>
                        Date submitted: {this.state.resource.timestamp}
                    </p>

                    <a href={this.state.resource.url} target="_blank">
                        <h4 className={styles.link}>
                            {this.state.resource.url}
                        </h4>
                    </a>

                    {this.state.resource.rating ? (
                        <Rating
                            icon="star"
                            defaultRating={this.state.resource.rating}
                            maxRating={5}
                            disabled
                            size="massive"
                        />
                    ) : (
                        <div></div>
                    )}
                    <Header as="h5" color="grey">
                        <Icon name="comment" />
                        <Header.Content>Comments:</Header.Content>
                    </Header>
                    <p style={{ color: "grey", marginTop: -10 }}>
                        {this.state.resource.comments}
                    </p>
                </Container>
            </div>
        );
    }
}
