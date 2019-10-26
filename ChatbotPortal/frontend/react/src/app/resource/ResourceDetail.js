import React, { Component } from "react";
import axios from "axios";
import {
    Header,
    Icon,
    Rating,
    Popup,
    Card,
    Container
} from "semantic-ui-react";

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
                    <Header
                        as="h3"
                        style={{
                            fontSize: "2em"
                        }}
                        color="blue"
                    >
                        Resource detail
                    </Header>
                    <a href={this.state.resource.url}>
                        <Header as="h3">
                            <Icon name="globe" />
                            <Header.Content>
                                {this.state.resource.title}
                            </Header.Content>
                        </Header>
                    </a>
                    <Header as="h5" color="grey">
                        Submitted by {this.state.resource.created_by_user}
                    </Header>
                    <Header as="h5" color="grey">
                        Created: {this.state.resource.timestamp}
                    </Header>
                    {this.state.resource.rating ? (
                        <Rating
                            icon="star"
                            defaultRating={this.state.resource.rating}
                            maxRating={5}
                            disabled
                        />
                    ) : (
                        <div></div>
                    )}
                    <Icon name="comment"></Icon> {this.state.resource.comments}
                </Container>
            </div>
        );
    }
}
